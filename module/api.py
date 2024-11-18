import inspect
import os
import importlib
from abc import ABC, abstractmethod
from typing import Optional


class Script(ABC):
    # 父类定义的必须覆盖的属性
    attributes = {
        # "name": str,
    }

    # 子类必须实现 run 方法
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    # 定义一个检查方法，用于验证子类是否覆盖了特定的属性
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr, attr_type in cls.attributes.items():
            # 检查子类是否覆盖属性
            if not hasattr(cls, attr):
                raise TypeError(
                    f"{cls.__name__} without an implementation for '{attr}'"
                )
            # 检查子类属性的类型是否匹配
            if not isinstance(getattr(cls, attr), attr_type):
                raise TypeError(
                    f"{cls.__name__} attr '{attr}' must be type {attr_type.__name__}"
                )


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
    script_list = get_scripts()
    for scripts in script_list.values():
        for Script in scripts:
            if name == Script.__name__:
                return Script
    return None
