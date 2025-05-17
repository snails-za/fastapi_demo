from typing import Optional

from fastapi import APIRouter, Depends
from redis import Redis
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import Q

from apps.dependencies.auth import get_current_user
from apps.form.device.device import DeviceOut, DeviceIn
from apps.models import Device, User
from apps.utils import response
from apps.utils.redis_ import RedisManager, get_redis_client

router = APIRouter(prefix="/device", tags=["设备管理"])

Device_Pydantic = pydantic_model_creator(Device, name="Device", exclude=("id",))


@router.post("/create", response_model=DeviceOut, summary="创建设备", description="创建设备接口")
async def create_device(device: DeviceIn):
    """
    创建设备
    :param device:
    :return:
    """
    # 检查设备是否存在
    if await Device.filter(name=device.name).exists():
        return response(code=400, message="设备已存在")
    # 创建设备
    device_obj = await Device.create(**device.model_dump(exclude_unset=True))
    data = await Device_Pydantic.from_tortoise_orm(device_obj)
    return response(data=data.model_dump())


@router.get("/list", response_model=list[Device_Pydantic], summary="设备列表", description="获取设备列表")
async def device_list(
        device_name: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        redis_client: Redis = Depends(get_redis_client),  # 自动注入
        user: User = Depends(get_current_user)
):
    """
    获取设备列表
    :return:
    """
    print(user.id)
    value = await redis_client.set('name', '222')
    print("=======")
    print(value)
    value = await redis_client.get('name')
    print(value)
    print("=======")
    conditions = []

    if device_name:
        conditions.append(Q(name__icontains=device_name))

    # 将组合条件传入 filter
    query = Device.filter(*conditions).order_by("-id").offset((page - 1) * page_size).limit(page_size)
    res = await Device_Pydantic.from_queryset(query)

    # 👇 显式调用 .model_dump() 以确保 jsonable_encoder 能生效
    data = [item.model_dump() for item in res]
    return response(data=data)
