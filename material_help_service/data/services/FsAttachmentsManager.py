import os
from hashlib import sha256
from typing import NoReturn

from data.services.BaseAttachmentsManager import BaseAttachmentsManager
from exceptions.AttachmentAlreadyCreatedException import AttachmentAlreadyCreatedException
from exceptions.AttachmentNotFoundException import AttachmentNotFoundException


class FsAttachmentsManager(BaseAttachmentsManager):
    def __init__(self):
        self._root = os.environ.get("ATTCH_ROOT")
    
    def delete(self, attachment_id: int) -> NoReturn:
        path_to_attch = self._generate_path(attachment_id)
        
        if not os.path.exists(path_to_attch):
            raise AttachmentNotFoundException()
        
        os.remove(path_to_attch)
        
    def create(self, attachment_id: int, content: bytes) -> NoReturn:
        path_to_attch = self._generate_path(attachment_id)
        
        if os.path.exists(path_to_attch):
            raise AttachmentAlreadyCreatedException()
        
        with open(path_to_attch, "wb") as file:
            file.write(content)

    def get_content(self, attachment_id: int) -> bytes:
        path_to_attch = self._generate_path(attachment_id)
        
        if not os.path.exists(path_to_attch):
            raise AttachmentNotFoundException()

        with open(path_to_attch, "rb") as file:
            return file.read()
    
    def _generate_path(self, attachment_id: int) -> str:
        hasher = sha256()
        hasher.update(str(attachment_id))
        id_hash = hasher.hexdigest().capitalize()
        
        res_path = self._root
        
        for i in range(0, len(id_hash) - 1):
            res_path += id_hash[i:i+2] + "/"
            
        res_path += f"{attachment_id}.attch"
        
        return res_path
        