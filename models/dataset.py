class Dataset:
    """Represents a dataset in the platform."""

    def __init__(self, dataset_id: int, name: str, rows: int, columns: int, uploaded_by: str, uploaded_at: str):
        self.__id = dataset_id
        self.__name = name
        self.__rows = rows
        self.__columns = columns
        self.__uploaded_by = uploaded_by
        self.__uploaded_at = uploaded_at

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_dimensions(self) -> tuple:
        """Returns (rows, columns)."""
        return self.__rows, self.__columns

    def get_uploaded_by(self) -> str:
        return self.__uploaded_by

    def get_uploaded_at(self) -> str:
        return self.__uploaded_at

    def __str__(self) -> str:
        return (
            f"Dataset {self.__id}: {self.__name} "
            f"({self.__rows} rows × {self.__columns} columns, "
            f"Uploaded by: {self.__uploaded_by} at {self.__uploaded_at})"
        )

