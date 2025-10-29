from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
import numpy as np
from datetime import datetime

# File Meta
file_meta = FileMetaDataset()
file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.1'  # CR Image Storage
file_meta.MediaStorageSOPInstanceUID = generate_uid()
file_meta.ImplementationClassUID = generate_uid()

# Dataset
ds = Dataset()
ds.file_meta = file_meta
ds.is_implicit_VR = False
ds.is_little_endian = True

# *** Patient Info - DEVE COMBINAR COM O WORKLIST ***
ds.PatientName = "SILVA^JOAO"
ds.PatientID = "99999"
ds.PatientBirthDate = "19850515"
ds.PatientSex = "M"

# Study Info
ds.StudyDescription = "RAIO-X TORAX PA/PERFIL"
ds.StudyInstanceUID = generate_uid()
ds.SeriesInstanceUID = generate_uid()
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.SOPClassUID = file_meta.MediaStorageSOPClassUID

# Series/Instance
ds.Modality = "CR"
ds.SeriesNumber = 1
ds.InstanceNumber = 1
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyTime = datetime.now().strftime('%H%M%S')
ds.AccessionNumber = ""

# Image Data (512x512 fake)
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.Rows = 512
ds.Columns = 512
ds.BitsAllocated = 16
ds.BitsStored = 12
ds.HighBit = 11
ds.PixelRepresentation = 0

# Pixel data (imagem fake com gradiente)
pixel_array = np.linspace(0, 4095, 512*512, dtype=np.uint16).reshape(512, 512)
ds.PixelData = pixel_array.tobytes()

# Salvar
ds.save_as('test-image.dcm', write_like_original=False)
print("✓ Imagem DICOM criada: test-image.dcm")