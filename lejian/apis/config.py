
from .model_wrapper import ModelWrapper


class ConfigWrapper(ModelWrapper):

    def as_dict(self):
        if self.type_ == 'bool':
            converter = bool
        elif self.type_ == 'string':
            converter = unicode
        elif self.type_ == 'int':
            converter = int
        elif self.type_ == 'float':
            converter = float
        else:
            converter = lambda v: v.strip() == '1'

        return {
            'id': self.id,
            'name': self.name,
            'brief': self.brief,
            'type': self.type_.code,
            'value': converter(self.value),
        }
