import PIL.Image
import modules
from modules import scripts, script_callbacks, shared
from modules.processing import process_images, Processed, StableDiffusionProcessingImg2Img
from modules.processing import Processed

from deepderpibooru.model import DeepDerpi
model = DeepDerpi(modules)

# Duck-typed class, based on `modules.interrogate.InterrogateModels`.
# Used to monkey-patch the singleton `modules.shared.interrogator`.
class FakeInterrogator:
    def __init__(self):
        self._derpi = DeepDerpi(modules)
    def load(self):
        self._derpi.load()
    def send_blip_to_ram(self):
        self._derpi.unload()
    def generate_caption(self, im: PIL.Image.Image):
        return self._derpi.predict(im)
    def interrogate(self, im: PIL.Image.Image):
        return self.generate_caption_lowvram(im)
    def generate_caption_lowvram(self, im: PIL.Image.Image):
        self.load()
        p = self._derpi.predict(im)
        self.send_blip_to_ram()
        return p
fake_interrogator = FakeInterrogator()

class DeepDerpibooruScript(scripts.Script):  
    # The title of the script. This is what will be displayed in the dropdown menu.
    def title(self):
        return "Interrogate DeepDerpibooru"

    # Determines when the script should be shown in the dropdown menu via the returned value.
    def show(self, is_img2img: bool) -> bool:
        return is_img2img

    # This is where the additional processing is implemented. The parameters include
    # self, the model object "p" (a StableDiffusionProcessing class, see
    # processing.py), and the parameters returned by the ui method.
    # Custom functions can be defined here, and additional libraries can be imported 
    # to be used in processing. The return value should be a Processed object, which is
    # what is returned by the process_images method.
    def run(self, p: StableDiffusionProcessingImg2Img) -> Processed:
        prediction = fake_interrogator.interrogate(p.init_images[0])
        p.do_not_save_samples = True
        p.do_not_save_grid = True
        p.steps = 0
        p.prompt = prediction
        proc = process_images(p)
        p.prompt = prediction

        return proc

def on_ui_settings():
    shared.opts.add_option("derpi_interrogator", shared.OptionInfo(True, "Replace CLIP Interrogator model with DeepDerpibooru (requires restart)", section=('interrogate', "Interrogate Options")))
def on_ui_tabs():
    if shared.opts.derpi_interrogator:
        shared.interrogator = fake_interrogator
script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_ui_tabs(on_ui_tabs)
