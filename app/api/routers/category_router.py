from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.docs.error_responses import (
    CREATE_RESPONSES,
    GET_BY_ID_RESPONSES,
    UPDATE_RESPONSES,
)
from app.api.messages.catalog import MessageKey, get_message
from app.api.schemas.category_schema import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from app.api.schemas.common_schema import ApiResponse
from app.application.use_cases.category.create_category import (
    CreateCategoryInput,
    CreateCategoryUseCase,
)
from app.application.use_cases.category.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.category.list_categories import ListCategoriesUseCase
from app.application.use_cases.category.update_category import (
    UpdateCategoryInput,
    UpdateCategoryUseCase,
)
from app.infrastructure.container import Container

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get(
    "",
    response_model=ApiResponse[list[CategoryResponse]],
    summary="Listar todas as categorias",
)
@inject
def list_categories(
    use_case: ListCategoriesUseCase = Depends(
        Provide[Container.list_categories_use_case]
    ),
) -> ApiResponse[list[CategoryResponse]]:
    categories = use_case.execute()
    responses = [CategoryResponse.model_validate(category) for category in categories]
    return ApiResponse(message=get_message(MessageKey.CATEGORY_LISTED), data=responses)


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
    input_data = CreateCategoryInput(**request.model_dump())
    new_category = use_case.execute(input_data)
    response = CategoryResponse.model_validate(new_category)
    return ApiResponse(message=get_message(MessageKey.CATEGORY_CREATED), data=response)


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
        message=get_message(MessageKey.CATEGORY_RETRIEVED), data=response
    )


@router.patch(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    summary="Atualizar detalhes de uma categoria",
    responses={**UPDATE_RESPONSES},
)
@inject
def update_category(
    category_id: int,
    request: CategoryUpdateRequest,
    use_case: UpdateCategoryUseCase = Depends(
        Provide[Container.update_category_use_case]
    ),  # noqa: E501
) -> ApiResponse[CategoryResponse]:
    input_data = UpdateCategoryInput(
        category_id, **request.model_dump(exclude_unset=True)
    )
    updated_category = use_case.execute(input_data)
    response = CategoryResponse.model_validate(updated_category)
    return ApiResponse(message=get_message(MessageKey.CATEGORY_UPDATED), data=response)
