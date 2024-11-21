import inspect
from abc import ABC, abstractmethod


class Script(ABC):
    # 父类定义的必须覆盖的属性
    attributes = {
        "name": str,
    }

    # 子类必须实现 run 方法
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def task(self, *args, **kwargs):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # 限制子类仅能覆盖 attributes 中的属性和 run 方法
        allowed_overrides = set(Script.attributes.keys()).union({"run"})

        # 检查子类定义的成员
        for name in cls.__dict__:
            if name not in allowed_overrides and not name.startswith("__"):
                raise TypeError(
                    f"{cls.__name__} is not allowed to override '{name}'. "
                    f"Only {', '.join(allowed_overrides)} can be overridden."
                )

        # 检查 attributes 中定义的属性是否被正确覆盖
        for attr, attr_type in cls.attributes.items():
            if not hasattr(cls, attr):
                raise TypeError(
                    f"{cls.__name__} is missing required attribute '{attr}'"
                )
            if not isinstance(getattr(cls, attr), attr_type):
                raise TypeError(
                    f"{cls.__name__} attribute '{attr}' must be of type {attr_type.__name__}"
                )

# 正确的子类
class MyScript(Script):
    name = "My Script"

    def run(self, *args, **kwargs):
        print("Running...")

# 不允许覆盖其他方法的子类
class InvalidScript(Script):
    name = "Invalid Script"

    def run(self, *args, **kwargs):
        print("Running...")

    def task(self):  # 尝试覆盖父类 task 方法
        pass

# 测试
try:
    valid_script = MyScript()
    print("MyScript is valid.")
except TypeError as e:
    print(e)

try:
    invalid_script = InvalidScript()
    print("InvalidScript is valid.")
except TypeError as e:
    print(e)