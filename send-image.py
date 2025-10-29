from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import ComputedRadiographyImageStorage
from pydicom import dcmread

# Ativar logs
debug_logger()

# Configurar
ae = AE(ae_title=b'RXSIMULATOR')
ae.add_requested_context(ComputedRadiographyImageStorage)

# Ler imagem
ds = dcmread('test-image.dcm')

print("\n=== Enviando Imagem para Orthanc (C-STORE) ===\n")

# Conectar
assoc = ae.associate('localhost', 4242, ae_title=b'ORTHANC')

if assoc.is_established:
    print("✓ Conectado ao ORTHANC\n")
    
    # Enviar imagem
    status = assoc.send_c_store(ds)
    
    if status:
        print(f"\n✓ Imagem enviada com sucesso!")
        print(f"Status: 0x{status.Status:04x}")
    else:
        print("✗ Falha no envio")
    
    assoc.release()
    print("\nConexão encerrada.")
else:
    print('✗ Falha ao conectar')

input("\nPressione ENTER para sair...")