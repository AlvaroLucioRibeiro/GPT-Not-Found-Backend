from typing import Optional
from db.db_base_classes import Product
from db.CRUD.create import create_product
from db.CRUD.update import update_product
from db.CRUD.delete import delete_product
from db.CRUD.read import get_product_by_id, get_all_products
from utils.utils_token_auth import get_current_user
from fastapi import APIRouter, HTTPException, status, Depends, Query, Body

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/")
async def get_products(
    product_id: Optional[int] = Query(
        None, description="The unique identifier of the product"
    ),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves a list of all available products or a specific product if 'product_id' is provided.

    Args:
        product_id (Optional[int]): The unique identifier of the product.
        current_user (dict): The authenticated user.

    Returns:
        dict or list: The product details if 'product_id' is provided, otherwise a list of all products.

    Raises:
        HTTPException: If the requested product is not found.
    """
    if product_id:
        product = await get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    return await get_all_products()


@products_router.post("/")
async def create_new_product(
    product: Product, current_user: dict = Depends(get_current_user)
):
    """
    Creates a new product in the system.

    Args:
        product (Product): The product details to be added.
        current_user (dict): The authenticated user.

    Returns:
        dict: Confirmation message along with the created product details.

    Raises:
        HTTPException: If the product creation fails.
    """
    try:
        new_product = await create_product(product.dict())
        return {"message": "Product created successfully!", "product": new_product}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating product: {str(exc)}",
        )


@products_router.put("/")
async def modify_product(
    product_id: int = Query(..., description="The unique identifier of the product"),
    product: Product = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Updates the details of an existing product.

    Args:
        product_id (int): The unique identifier of the product.
        product (Product): The updated product data.
        current_user (dict): The authenticated user.

    Returns:
        dict: Confirmation message with updated product details.

    Raises:
        HTTPException: If the product is not found or the update fails.
    """
    existing_product = await get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await update_product(product_id, product.dict())
    if not updated_product:
        raise HTTPException(status_code=500, detail="Product update failed")

    return {"message": "Product updated successfully", "product": updated_product}


@products_router.delete("/")
async def remove_product(
    product_id: int = Query(..., description="The unique identifier of the product"),
    current_user: dict = Depends(get_current_user),
):
    """
    Deletes a product from the system.

    Args:
        product_id (int): The unique identifier of the product to be deleted.
        current_user (dict): The authenticated user.

    Returns:
        dict: Confirmation message upon successful deletion.

    Raises:
        HTTPException: If the product is not found or deletion fails.
    """
    existing_product = await get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    deleted = await delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Product could not be deleted")

    return {"message": "Product deleted successfully"}
