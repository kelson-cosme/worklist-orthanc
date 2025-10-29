from flask import Flask, request, jsonify
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from datetime import datetime
import os
import uuid

app = Flask(__name__)

WORKLIST_DIR = "/worklists"

def generate_worklist_file(data):
    """
    Gera um arquivo DICOM Worklist (.wl) com os dados fornecidos.
    """
    # File Meta Information
    file_meta = FileMetaDataset()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.31'  # Modality Worklist SOP Class
    file_meta.MediaStorageSOPInstanceUID = generate_uid()  # UID válido e curto
    file_meta.ImplementationClassUID = generate_uid()
    
    # Dataset principal
    ds = Dataset()
    ds.file_meta = file_meta
    ds.is_implicit_VR = False
    ds.is_little_endian = True
    
    # Specific Character Set
    ds.SpecificCharacterSet = 'ISO_IR 100'
    
    # Patient Information
    ds.PatientName = data.get('patientName', '')
    ds.PatientID = data.get('patientId', '')
    ds.PatientBirthDate = data.get('patientBirthDate', '').replace('-', '')
    ds.PatientSex = data.get('patientSex', 'O')
    
    # Study Information
    ds.AccessionNumber = data.get('accessionNumber', '')
    ds.StudyInstanceUID = generate_uid()  # Gera UID válido (máx 64 chars)
    ds.StudyDescription = data.get('studyDescription', '')
    ds.RequestingPhysician = data.get('requestingPhysician', '')
    ds.InstitutionName = "SERVIOCLIN SERVICOS RADIOLOGICOS"
    
    # Scheduled Procedure Step Sequence
    sps = Dataset()
    sps.Modality = data.get('modality', 'CR')
    sps.ScheduledStationAETitle = "ANY"
    
    # Data e Hora
    scheduled_date = data.get('scheduledProcedureStepStartDate', '')
    if scheduled_date:
        sps.ScheduledProcedureStepStartDate = scheduled_date.replace('-', '')
    else:
        sps.ScheduledProcedureStepStartDate = datetime.now().strftime('%Y%m%d')
    
    scheduled_time = data.get('scheduledProcedureStepStartTime', '')
    if scheduled_time:
        sps.ScheduledProcedureStepStartTime = scheduled_time.replace(':', '') + '00'
    else:
        sps.ScheduledProcedureStepStartTime = datetime.now().strftime('%H%M%S')
    
    sps.ScheduledProcedureStepDescription = data.get('procedureDescription', data.get('studyDescription', ''))
    sps.ScheduledProcedureStepID = str(uuid.uuid4())[:8]
    
    # Adiciona a sequência ao dataset principal
    ds.ScheduledProcedureStepSequence = [sps]
    
    # Requested Procedure ID e Scheduled Procedure Step ID
    ds.RequestedProcedureID = str(uuid.uuid4())[:8]
    
    # Gera nome único para o arquivo
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    patient_id = data.get('patientId', 'unknown').replace(' ', '_')
    filename = f"{patient_id}_{timestamp}.wl"
    filepath = os.path.join(WORKLIST_DIR, filename)
    
    # Salva o arquivo com Transfer Syntax explícito
    ds.save_as(filepath, write_like_original=False)
    
    return filename

@app.route('/create-worklist', methods=['POST'])
def create_worklist():
    """
    Endpoint para criar um item de worklist.
    Espera JSON com os dados do exame.
    """
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('patientId') or not data.get('patientName'):
            return jsonify({'error': 'patientId e patientName são obrigatórios'}), 400
        
        filename = generate_worklist_file(data)
        
        return jsonify({
            'success': True,
            'message': 'Worklist item criado com sucesso',
            'filename': filename
        }), 201
        
    except Exception as e:
        app.logger.error(f"Erro ao criar worklist: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Cria o diretório de worklists se não existir
    os.makedirs(WORKLIST_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=8002, debug=True)