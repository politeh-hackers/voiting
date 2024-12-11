class FilterErrorMessages:
    REQUIRED = "Поле '{field_name}' обязательно.",
    LENGTH = "Поле '{field_name}' должно содержать от {min_length} до {max_length} символов.",
    NUMBER_ERROR = "Номер должен содержать только цифры и начинаться с +375"
    NAME_ERROR = "ФИО должны содержать только символы"
    FILE_TOO_LARGE = "Файл слишком большой. Максимальный размер: {MAX_PHOTO_SIZE_MB} МБ.",
    IMAGE_DEMENSIONS = "Размер изображения должен быть не больше {MAX_PHOTO_WIDTH}x{MAX_PHOTO_HEIGHT} пикселей."
    

    # ERROR_MESSAGES = {
    # "date_format": "Дата должна быть в формате {date_format}.",
    # "invalid_tags": "Неверные теги: {tags}.",
    # "not_image": "Файл должен быть изображением.",
    # "file_name_too_long": f"Слишком длинное имя файла. Максимальная длина: {MAX_PHOTO_NAME_LENGTH} символов.",
    # "password_too_short": f"Пароль должен содержать минимум {PASSWORD_MIN_LENGTH} символов.",
    # "password_no_digit": "Пароль должен содержать хотя бы одну цифру.",
    # "password_no_special": f"Пароль должен содержать хотя бы один специальный символ из {SPECIAL_CHARACTERS}.",
