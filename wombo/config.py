not_imported = []

try:
    from PIL.Image import Image
except ModuleNotFoundError:
    not_imported.append("pillow")