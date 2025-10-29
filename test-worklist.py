#!/usr/bin/env python3
from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset

# Configurar Application Entity
ae = AE(ae_title=b'RXSIMULATOR')
ae.add_requested_context(ModalityWorklistInformationFind)

# Query
ds = Dataset()
ds.PatientName = ''
ds.PatientID = ''
ds.PatientBirthDate = ''
ds.PatientSex = ''
ds.AccessionNumber = ''
ds.StudyDescription = ''

ds.ScheduledProcedureStepSequence = [Dataset()]
ds.ScheduledProcedureStepSequence[0].Modality = ''
ds.ScheduledProcedureStepSequence[0].ScheduledStationAETitle = ''
ds.ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartDate = ''
ds.ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartTime = ''
ds.ScheduledProcedureStepSequence[0].ScheduledProcedureStepDescription = ''

print("\n=== Consultando Worklist no Orthanc ===\n")

# ALTERE AQUI PARA SEU IP/DOMÍNIO
assoc = ae.associate('localhost', 4242, ae_title=b'ORTHANC')

if assoc.is_established:
    print("✓ Conectado ao ORTHANC\n")
    
    responses = assoc.send_c_find(ds, ModalityWorklistInformationFind)
    
    count = 0
    for (status, identifier) in responses:
        if status:
            if status.Status in (0xFF00, 0xFF01):
                count += 1
                print(f"\n{'='*50}")
                print(f"  ITEM {count} DA WORKLIST")
                print('='*50)
                print(f"Paciente: {identifier.PatientName}")
                print(f"ID: {identifier.PatientID}")
                print(f"Data Nasc: {identifier.PatientBirthDate}")
                print(f"Sexo: {identifier.PatientSex}")
                
                if hasattr(identifier, 'ScheduledProcedureStepSequence'):
                    sps = identifier.ScheduledProcedureStepSequence[0]
                    print(f"\nAgendamento:")
                    print(f"  Modalidade: {sps.Modality}")
                    print(f"  Data: {sps.ScheduledProcedureStepStartDate}")
                    print(f"  Hora: {sps.ScheduledProcedureStepStartTime}")
                    print(f"  Descrição: {sps.get('ScheduledProcedureStepDescription', 'N/A')}")
            elif status.Status == 0x0000:
                print(f"\n{'='*50}")
                print("✓ Consulta finalizada")
                print('='*50)
    
    if count == 0:
        print("\n⚠ Nenhum item na worklist")
    else:
        print(f"\n✓ Total: {count} item(ns)")
    
    assoc.release()
else:
    print('✗ Falha ao conectar')
    print('Verifique firewall e porta 4242')

input("\nPressione ENTER para sair...")