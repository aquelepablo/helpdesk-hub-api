from fastapi import APIRouter, status

from app.adapters.http.docs.error_responses import (
    CREATE_RESPONSES,
    GET_BY_ID_RESPONSES,
    UPDATE_RESPONSES,
)
from app.adapters.http.mappers.category_mapper import (
    to_create_category_input,
    to_update_category_input,
)
from app.adapters.http.schemas.category_schema import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from app.adapters.http.schemas.common_schema import ApiResponse
from app.application.use_cases.category.create_category import CreateCategoryUseCase
from app.application.use_cases.category.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.category.list_categories import ListCategoriesUseCase
from app.application.use_cases.category.update_category import UpdateCategoryUseCase
from app.domain.repositories.category_repository import CategoryRepository
from app.infra.db.repositories.category_repository import InMemoryCategoryRepository

router = APIRouter(prefix="/category", tags=["categories"])


def _get_category_repository() -> CategoryRepository:
    return InMemoryCategoryRepository()


@router.get(
    "",
    response_model=ApiResponse[list[CategoryResponse]],
    summary="Listar todas as categorias",
)
def list_categories() -> ApiResponse[list[CategoryResponse]]:
    list_categories_use_case = ListCategoriesUseCase(_get_category_repository())
    categories = list_categories_use_case.execute()
    responses = [CategoryResponse.model_validate(category) for category in categories]

    return ApiResponse(
        message="Listagem de categorias realizada com sucesso", data=responses
    )


@router.post(
    "",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
    responses={**CREATE_RESPONSES},
)
def create_category(request: CategoryCreateRequest) -> ApiResponse[CategoryResponse]:
    input_data = to_create_category_input(request)
    create_category_use_case = CreateCategoryUseCase(_get_category_repository())
    new_category = create_category_use_case.execute(input_data)
    response = CategoryResponse.model_validate(new_category)
    return ApiResponse(message="Categoria criada com sucesso", data=response)


@router.get(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    summary="Obter detalhes de uma categoria",
    responses={**GET_BY_ID_RESPONSES},
)
def get_category_by_id(category_id: int) -> ApiResponse[CategoryResponse]:
    get_category_by_id_use_case = GetCategoryByIdUseCase(_get_category_repository())
    category = get_category_by_id_use_case.execute(category_id)
    response = CategoryResponse.model_validate(category)

    return ApiResponse(
        message="Detalhes da categoria obtidos com sucesso", data=response
    )


@router.patch(
    "",
    response_model=ApiResponse[CategoryResponse],
    summary="Atualizar detalhes de uma categoria",
    responses={**UPDATE_RESPONSES},
)
def update_category(request: CategoryUpdateRequest) -> ApiResponse[CategoryResponse]:
    input_data = to_update_category_input(request)
    update_category_use_case = UpdateCategoryUseCase(_get_category_repository())
    updated_category = update_category_use_case.execute(input_data)
    response = CategoryResponse.model_validate(updated_category)
    return ApiResponse(message="Categoria atualizada com sucesso", data=response)
