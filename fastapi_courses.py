from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, RootModel, Field

# Pydantic модели
class CourseIn(BaseModel):
    """
    Входная модель для создания и обновления курса.
    Не содержит поле id (генерируется автоматически).
    """
    title: str = Field(..., min_length=1, max_length=200, description="Название курса")
    max_score: int = Field(..., ge=1, le=100, description="Максимальный балл (1-100)")
    min_score: int = Field(..., ge=0, le=100, description="Минимальный проходной балл (0-100)")
    description: str = Field(..., min_length=1, max_length=1000, description="Краткое описание курса")

    def model_post_init(self, __context):
        """Валидация: min_score не может быть больше max_score"""
        if self.min_score > self.max_score:
            raise ValueError(f"min_score ({self.min_score}) cannot be greater than max_score ({self.max_score})")


class CourseOut(CourseIn):
    """
    Выходная модель для отдачи данных о курсе.
    Включает поле id (уникальный идентификатор).
    """
    id: int = Field(..., description="Уникальный идентификатор курса")


# In-memory хранилище с использованием RootModel

class CoursesStore(RootModel):
    """
    Хранилище курсов в оперативной памяти.
    Наследуется от RootModel для совместимости с Pydantic v2.
    """
    root: list[CourseOut] = Field(default_factory=list, description="Список всех курсов")

    def find(self, course_id: int) -> CourseOut | None:
        """
        Находит курс по ID.

        Args:
            course_id: ID курса для поиска

        Returns:
            CourseOut | None: Найденный курс или None, если не найден
        """
        for course in self.root:
            if course.id == course_id:
                return course
        return None

    def create(self, course_in: CourseIn) -> CourseOut:
        """
        Создаёт новый курс с автоматической генерацией ID.

        Args:
            course_in: Входные данные курса

        Returns:
            CourseOut: Созданный курс с присвоенным ID
        """
        # Генерируем новый ID (на основе длины списка + 1)
        new_id = len(self.root) + 1
        course = CourseOut(id=new_id, **course_in.model_dump())
        self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        """
        Обновляет существующий курс по ID.

        Args:
            course_id: ID курса для обновления
            course_in: Новые данные курса

        Returns:
            CourseOut: Обновлённый курс

        Raises:
            IndexError: Если курс с указанным ID не найден
        """
        # Находим индекс курса по ID
        index = next(
            (idx for idx, course in enumerate(self.root) if course.id == course_id),
            None
        )
        if index is None:
            raise IndexError(f"Course with id {course_id} not found")

        # Создаём обновлённый объект
        updated_course = CourseOut(id=course_id, **course_in.model_dump())
        self.root[index] = updated_course
        return updated_course

    def delete(self, course_id: int) -> None:
        """
        Удаляет курс по ID.

        Args:
            course_id: ID курса для удаления

        Raises:
            IndexError: Если курс с указанID не найден
        """
        index = next(
            (idx for idx, course in enumerate(self.root) if course.id == course_id),
            None
        )
        if index is None:
            raise IndexError(f"Course with id {course_id} not found")

        self.root.pop(index)


# Инициализация приложения и роутера

# Создаём FastAPI приложение
app = FastAPI(
    title="Courses API",
    description="CRUD API для управления курсами",
    version="1.0.0"
)

# Создаём роутер с префиксом и тегом
courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"]
)

# Инициализируем хранилище
store = CoursesStore(root=[])


# CRUD эндпоинты

@courses_router.get(
    "/{course_id}",
    response_model=CourseOut,
    summary="Получить курс по ID",
    description="Возвращает курс с указанным идентификатором"
)
async def get_course(course_id: int):
    """
    GET /api/v1/courses/{course_id}

    Получает курс по его ID.

    Args:
        course_id: Уникальный идентификатор курса

    Returns:
        CourseOut: Данные курса

    Raises:
        404: Если курс с указанным ID не найден
    """
    course = store.find(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course


@courses_router.get(
    "",
    response_model=list[CourseOut],
    summary="Получить список всех курсов",
    description="Возвращает массив всех курсов в системе"
)
async def get_courses():
    """
    GET /api/v1/courses

    Получает список всех курсов.

    Returns:
        list[CourseOut]: Массив всех курсов
    """
    return store.root


@courses_router.post(
    "",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый курс",
    description="Создаёт новый курс с автоматической генерацией ID"
)
async def create_course(course: CourseIn):
    """
    POST /api/v1/courses

    Создаёт новый курс. ID генерируется автоматически.

    Args:
        course: Входные данные курса (без ID)

    Returns:
        CourseOut: Созданный курс с присвоенным ID
    """
    return store.create(course)


@courses_router.put(
    "/{course_id}",
    response_model=CourseOut,
    summary="Обновить курс",
    description="Обновляет существующий курс по ID"
)
async def update_course(course_id: int, course: CourseIn):
    """
    PUT /api/v1/courses/{course_id}

    Обновляет данные существующего курса.

    Args:
        course_id: ID курса для обновления
        course: Новые данные курса

    Returns:
        CourseOut: Обновлённый курс

    Raises:
        404: Если курс с указанным ID не найден
    """
    try:
        return store.update(course_id, course)
    except IndexError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@courses_router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить курс",
    description="Удаляет курс по ID"
)
async def delete_course(course_id: int):
    """
    DELETE /api/v1/courses/{course_id}

    Удаляет курс по ID.

    Args:
        course_id: ID курса для удаления

    Raises:
        404: Если курс с указанным ID не найден
    """
    try:
        store.delete(course_id)
    except IndexError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    # 204 No Content - тело ответа пустое


# Подключение роутера к приложению

app.include_router(courses_router)

# Программный запуск

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "fastapi_courses:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )