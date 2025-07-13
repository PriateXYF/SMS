import inspect
import os
import re
import importlib
from abc import ABC, abstractmethod
from typing import Optional, get_origin, get_args, Annotated

from sqlalchemy.util import OrderedDict


# 将脚本类名解析为脚本名称
def parse_classname(s : str):
    # 在大写字母前加分隔符（保留数字作为整体）
    parts = re.findall(r'[A-Z]?[a-z]+|\d+', s)
    return '-'.join(part.lower() for part in parts if part)

class Script(ABC):
    # 父类定义的必须覆盖的属性
    attributes = {
        "name": str,
    }
    # run 方法中的参数列表
    params = []

    # 子类必须实现 run 方法
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
    # 实际上父类执行的方法
    def do(self, *args, **kwargs):
        return self.run(*args, **kwargs)
    
    def help(self):
        usage = f"""Usage: sms.py use {self.name} [OPTIONS]\n\n\t{self.__doc__}\n
Options:\n\t--{"\n\t--".join([ f'{param[0]} [{param[1].__name__}] {param[2][0]} {"" if param[3] is None else f"(default:{param[3]})"}' for param in self.params ])}
        """
        print(usage)

    @classmethod
    def get_args(cls):
        """获取所有参数列表"""
        signature = inspect.signature(cls.run)
        parameters = signature.parameters
        params = parameters.copy()
        params.pop('self', None)
        return params
    # 定义一个检查方法，用于验证子类是否覆盖了特定的属性
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 限制子类仅能覆盖 attributes 中的属性和 run 方法
        allowed_overrides = set(Script.attributes.keys()).union({"run"})
        # 检查子类定义的成员
        for name in cls.__dict__:
            if name not in allowed_overrides and not name.startswith(f"_{cls.__name__}") and not name.startswith(f"__"):
                raise TypeError(
                    f"{cls.__name__} is not allowed to override '{name}'. "
                    f"Only {', '.join(allowed_overrides)} can be overridden."
                )
        # 如果未设置脚本名称则自动解析类名
        if not hasattr(cls, 'name'):
            setattr(cls, 'name', parse_classname(cls.__name__))
        else:
            cls.name = cls.name.lower()
        # 检查 attributes 中定义的属性是否被正确覆盖
        for attr, attr_type in cls.attributes.items():
            if not hasattr(cls, attr):
                raise TypeError(f"{cls.__name__} is missing required attribute '{attr}'")
            if not isinstance(getattr(cls, attr), attr_type):
                raise TypeError(
                    f"{cls.__name__} attribute '{attr}' must be of type {attr_type.__name__}"
                )
        # 手动检查子类是否实现了抽象方法 run 并确保它是方法
        run_method = getattr(cls, 'run', None)
        if run_method == Script.run or not callable(run_method):
            raise TypeError(f"{cls.__name__} must implement the abstract method 'run'.")
        # 检查 run 函数参数是否对应正确
        signature = inspect.signature(run_method)
        parameters = signature.parameters
        cls.params = []
        for key, attr in parameters.items():
            if key == "self":
                continue
            annotation = attr.annotation
                # 检查是否为 Annotated 类型
            if get_origin(annotation) is Annotated:
                basetype = get_args(annotation)[0]  # 提取基础类型
                metadata = get_args(annotation)[1:]  # 提取备注
                defaultval = None if attr.default is inspect._empty else attr.default
                cls.params.append((key, basetype, metadata, defaultval))
            else:
                raise TypeError(f"{cls.__name__} 'run' param '{key}' must be Annotated")
# 获取所有的脚本列表
def get_scripts() -> dict:
    
    scripts_path = os.path.join(os.path.dirname(__file__), "../scripts")
    script_classes = {}

    # 遍历 scripts 目录
    for root, _, files in os.walk(scripts_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                module_name = (
                    os.path.relpath(file_path, scripts_path)
                    .replace(os.sep, ".")
                    .rstrip(".py")
                )
                # 动态加载模块
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 检查模块中的类
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Script) and obj is not Script:
                        relative_folder = os.path.relpath(root, scripts_path)
                        if relative_folder not in script_classes:
                            script_classes[relative_folder] = []
                        script_classes[relative_folder].append(obj)
    return script_classes


# 通过脚本名获取脚本
def get_script(name: str) -> Optional[Script]:
    name = name.lower()
    script_list = get_scripts()
    for scripts in script_list.values():
        for Script in scripts:
            if name == Script.name:
                return Script
    return None
