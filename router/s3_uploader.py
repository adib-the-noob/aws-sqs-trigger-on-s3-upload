from fastapi import UploadFile, File
from fastapi.routing import APIRouter
from utils.s3_utils import s3_client

router = APIRouter()


@router.post('/upload-video')
async def upload_video(file: UploadFile = File(...)):
    try:
        response = s3_client.create_multipart_upload(
            Bucket='adib-source-bucket',
            Key=file.filename,
            ContentType=file.content_type
        )

        upload_id = response['UploadId']
        
        parts = []
        part_number = 1
        chunk_size = 5 * 1024 * 1024
        
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            part = s3_client.upload_part(
                Bucket='adib-source-bucket',
                Key=file.filename,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk
            )
            parts.append({
                'PartNumber': part_number,
                'ETag': part['ETag'] # Etage is a unique identifier for the part
            })
            part_number += 1    
            
        s3_client.complete_multipart_upload(
            Bucket='adib-source-bucket',
            Key=file.filename,
            UploadId=upload_id,
            MultipartUpload={
                'Parts': parts
            }
        )
        
        return {
            "message": "Video uploaded successfully",
            "filename": file.filename,
            "url": f"https://adib-source-bucket.s3.amazonaws.com/{file.filename}"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "An error occured",
            "error": str(e)
        }