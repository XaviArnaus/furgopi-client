class BaseEntity:

    @property
    def name(self):
        raise NotImplementedError("The [name] property is not implemented.")

    def to_string(self) -> str:
        raise NotImplementedError("The [to_string] method is not implemented.")
    
    def from_dict():
        raise NotImplementedError("The [from_dict] method is not implemented.")
    
    def to_dict(self) -> dict:
        raise NotImplementedError("The [to_dict] method is not implemented.")