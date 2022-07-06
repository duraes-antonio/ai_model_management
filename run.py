from main.services.local_results_storage_service import LocalResultsStorageService
from main.unet.unet import make_unet

unet = make_unet(3)

storage = LocalResultsStorageService[int]()
axt = storage.get('')
