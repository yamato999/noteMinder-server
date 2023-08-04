from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_note(self, user_id: str, payload: dict, title: str):
        payload["user_id"] = ObjectId(user_id)
        payload["title"] = title
        note = self.database["notes"].insert_one(payload)
        return note.inserted_id
    
    def create_tags(self, user_id: str, payload: dict, title: str):
        payload["user_id"] = ObjectId(user_id)
        payload["title"] = title
        note = self.database["tags"].insert_one(payload)
        return note.inserted_id

    def get_note_by_id(self, note_id: str, user_id: str) -> Optional[dict]:
        user = self.database["notes"].find_one(
            {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
        )
        return user

    def get_all_notes(self, user_id: str) -> List[dict]:
        notes = self.database["notes"].find({"user_id": ObjectId(user_id)})
        return list(notes)
    
    def update_note_by_id(self, note_id: str, user_id: str, data: dict) -> UpdateResult:
        return self.database["notes"].update_one(
            filter={"_id": ObjectId(note_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak_by_id(self, note_id: str, user_id: str) -> DeleteResult:
        return self.database["notes"].delete_one(
            {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
        )