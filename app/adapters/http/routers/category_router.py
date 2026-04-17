from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

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
from app.infra.container import Container

router = APIRouter(prefix="/category", tags=["categories"])


@router.get(
    "",
    response_model=ApiResponse[list[CategoryResponse]],
    summary="Listar todas as categorias",
)
@inject
def list_categories(
    use_case: ListCategoriesUseCase = Depends(
        Provide[Container.list_categories_use_case]
    ),  # noqa: E501
) -> ApiResponse[list[CategoryResponse]]:
    categories = use_case.execute()
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
@inject
def create_category(
    request: CategoryCreateRequest,
    use_case: CreateCategoryUseCase = Depends(
        Provide[Container.create_category_use_case]
    ),  # noqa: E501
) -> ApiResponse[CategoryResponse]:
    input_data = to_create_category_input(request)
    new_category = use_case.execute(input_data)
    response = CategoryResponse.model_validate(new_category)
    return ApiResponse(message="Categoria criada com sucesso", data=response)


@router.get(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    summary="Obter detalhes de uma categoria",
    responses={**GET_BY_ID_RESPONSES},
)
@inject
def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(
        Provide[Container.get_category_by_id_use_case]
    ),  # noqa: E501
) -> ApiResponse[CategoryResponse]:
    category = use_case.execute(category_id)
    response = CategoryResponse.model_validate(category)
    return ApiResponse(
        message="Detalhes da categoria obtidos com sucesso", data=response
    )


@router.patch(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    summary="Atualizar detalhes de uma categoria",
    responses={**UPDATE_RESPONSES},
)
@inject
def update_category(
    request: CategoryUpdateRequest,
    use_case: UpdateCategoryUseCase = Depends(
        Provide[Container.update_category_use_case]
    ),  # noqa: E501
) -> ApiResponse[CategoryResponse]:
    input_data = to_update_category_input(request)
    updated_category = use_case.execute(input_data)
    response = CategoryResponse.model_validate(updated_category)
    return ApiResponse(message="Categoria atualizada com sucesso", data=response)
