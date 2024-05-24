from .export_shapes import export_shapes

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(export_shapes(Krita.instance()))
