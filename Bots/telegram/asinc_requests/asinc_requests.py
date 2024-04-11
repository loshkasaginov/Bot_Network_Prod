import json
from Bots.logger.logger import logger
import aiohttp
import asyncio
from json import *
import aiofiles
from Bots.DB.sqlite_db import Db

base_url = 'http://127.0.0.1:8000/'
async def super_user_auth(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'auth/register/SuperUser'
        async with session.post(url, json=data) as response:
            if response.status == 201:
                logger.info(f'user {data["user_name"]} super_user_auth status: {response.status}')
                await auth_get_access_token(data,link)
                return True
            response_json = await response.json()
            logger.warn(f'user {link} super_user_auth status {response.status} details: {response_json["detail"]}')
    return False



async def auth_get_access_token(data:dict, link:str):
    async with aiohttp.ClientSession() as session:
        token_url = base_url + 'auth/access-token'
        logger.info(f'user {data["user_name"]} auth_get_access_token')
        async with session.post(token_url, data={"username": data["user_name"], "password": data["password"]}) as token_response:
            logger.info(f'user {data["user_name"]} auth_get_access_token status: {token_response.status}')
            response_json = await token_response.json()
            db = Db()
            await db.insert_users(link,data["user_name"], response_json["access_token"], response_json["refresh_token"])

async def refresh_access_tokens():
    pass
    # db = Db()
    # users = await db.get_all_user_ids_and_refresh_tokens()
    # for user in users:
    #     async with aiohttp.ClientSession() as session:
    #         token_url = base_url + 'auth/refresh-token'
    #         print(user[1])
    #         data = {
    #             "refresh_token": str(user[1])
    #         }
    #         headers = {'Content-Type': 'application/json'}
    #         print(type(data))
    #         str_data = json.dumps(data)
    #         json_data = json.loads(str_data)
    #         async with session.post(token_url, json=data) as token_response:
    #             print(token_response)
    #             response_json = print()
    #             print(response_json)
    #             print(token_response)
    #             await db.update_access_token(user[0], response_json["refresh_token"], response_json["access_token"])

async def get_headers(link:str):
    db = Db()
    access_token = await db.get_access_token(link)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers

async def create_tutor(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'tutors/create/tutor'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {link} create_tutor status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} create_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def get_tutors(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'tutors/get_list/'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {link} get_tutors status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {link} get_tutors status {response.status} details: {response_json["detail"]}')
            return False

async def del_tutor(name:str, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}tutors/delete/{name}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {link} del_tutor status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} del_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def tutor_auth(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'auth/register/tutor'
        async with session.post(url, json=data) as response:
            if response.status == 201:
                logger.info(f'user {link} tutor_auth status OK (201)')
                await auth_get_access_token(data,link)
                return True
    response_json = await response.json()
    logger.warn(f'user {link} tutor_auth status {response.status} details: {response_json["detail"]}')
    return False

async def create_engineer(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'engineers/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {link} create_engineer status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} create_engineer status {response.status} details: {response_json["detail"]}')
            return False


async def get_engineers(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'engineers/get_list/'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {link} get_engineers status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {link} get_engineers status {response.status} details: {response_json["detail"]}')
            return False


async def del_engineer(engineers_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}engineers/delete/{engineers_number}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {link} del_engineer status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} del_engineer status {response.status} details: {response_json["detail"]}')
            return False


async def create_order(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'orders/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {link} create_order status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} create_order status {response.status} details: {response_json["detail"]}')
            return False


async def engineer_auth(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'auth/register/engineer'
        async with session.post(url, json=data) as response:
            if response.status == 201:
                logger.info(f'user {link} engineer_auth status OK (201)')
                await auth_get_access_token(data,link)
                return True
            response_json = await response.json()
            logger.warn(f'user {link} engineer_auth status {response.status} details: {response_json["detail"]}')
    return False


async def get_agreement_orders_engineer(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/agreement'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {link} get_agreement_orders_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {link} get_agreement_orders_engineer status {response.status} details: {response_json["detail"]}')
            return False


async def create_agreement(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'agreement/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {link} create_agreement status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} create_agreement status {response.status} details: {response_json["detail"]}')
            return False


async def get_prepayment_orders_engineer(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/prepayment'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:

            if response.status == 200:
                logger.info(f'user {link} get_prepayment_orders_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {link} get_prepayment_orders_engineer status {response.status} details: {response_json["detail"]}')
            return False


async def create_prepayment(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'prepayment/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {link} create_prepayment status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} create_prepayment status {response.status} details: {response_json["detail"]}')
            return False

async def get_short_orders_by_tutor(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'orders/get/short'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_short_orders_by_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {str(link)} get_short_orders_by_tutor status {response.status}, details: {response_json["detail"]}')
            return False


async def get_full_order_by_tutor(order_number:int, link:str):
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}orders/get/{order_number}'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_full_order_by_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_full_order_by_tutor status {response.status}, details: {response_json["detail"]}')
            return False


async def get_current_engineer_by_tutor(engineers_number:int, link:str):
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}engineers/get/{engineers_number}'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_current_engineer_by_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_current_engineer_by_tutor status {response.status}, details: {response_json["detail"]}')
            return False


async def get_outlay_orders_engineer(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/outlay_record'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_outlay_orders_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_outlay_orders_engineer status {response.status}, details: {response_json["detail"]}')
            return False


async def create_outlay_record(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'outlay_record/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} create_outlay_record status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} create_outlay_record status {response.status}, details: {response_json["detail"]}')
            return False


async def get_report_orders_engineer(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/report'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_report_orders_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_report_orders_engineer status {response.status}, details: {response_json["detail"]}')
            return False

async def create_report(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'report/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} create_report status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} create_report status {response.status}, details: {response_json["detail"]}')
            return False


async def state_engineer_auth(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'auth/register/state_engineer'
        async with session.post(url, json=data) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} state_engineer_auth status OK (201)')
                await auth_get_access_token(data,link)
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} state_engineer_auth status {response.status}, details: {response_json["detail"]}')
    return False


async def create_state_engineer(data:dict, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'state_engineers/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} create_state_engineer status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} create_state_engineer status {response.status}, details: {response_json["detail"]}')
            return False

async def del_state_engineer(state_engineer_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}state_engineers/delete/{state_engineer_number}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {str(link)} del_state_engineer status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} del_state_engineer status {response.status}, details: {response_json["detail"]}')
            return False

async def get_state_engineers(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'state_engineers/get_list/'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_state_engineers status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_state_engineers status {response.status}, details: {response_json["detail"]}')
            return False


async def get_current_state_engineer_by_tutor(engineers_number:int, link:str):
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}state_engineers/get/{engineers_number}'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_current_state_engineer_by_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_current_state_engineer_by_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def create_stationary(data: dict, link: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = base_url + 'stationary/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} create_stationary status OK (200)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} create_stationary status {response.status}, details: {response_json["detail"]}')
            return False

async def get_stationary_orders_engineer(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/stationary'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:

            if response.status == 200:
                logger.info(f'user {str(link)} get_stationary_orders_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stationary_orders_engineer status {response.status}, details: {response_json["detail"]}')
            return False


async def get_all_stationary_orders_state_engineer(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/stationary/not_assigned/state_engineer'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_all_stationary_orders_state_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_all_stationary_orders_state_engineer status {response.status}, details: {response_json["detail"]}')
            return False


async def put_current_stationary_by_state_engineer(order_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}stationary_by_state_eng/take_stationary/{order_number}'
        headers = await get_headers(link)
        async with session.put(url, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} put_current_stationary_by_state_engineer status OK (200)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} put_current_stationary_by_state_engineer status {response.status}, details: {response_json["detail"]}')
            return False

async def get_personal_stationary_orders_state_engineer(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/stationary/assigned/state_engineer'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_personal_stationary_orders_state_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_personal_stationary_orders_state_engineer status {response.status}, details: {response_json["detail"]}')
            return False


async def end_current_stationary_by_state_engineer(data: dict, link: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}stationary_by_state_eng/add_amount/'
        headers = await get_headers(link)
        async with session.put(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} end_current_stationary_by_state_engineer status OK (200)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} end_current_stationary_by_state_engineer status {response.status}, details: {response_json["detail"]}')
            return False


async def get_stationary_orders_tutor(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'get_order_by_stage/stationary/tutor'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_stationary_orders_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stationary_orders_tutor status {response.status}, details: {response_json["detail"]}')
            return False




async def change_priority_stationary_tutor(data: dict, link: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}stationary_by_state_eng/add_priority/'
        headers = await get_headers(link)
        async with session.put(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} get_stationary_orders_tutor status OK (200)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stationary_orders_tutor status {response.status}, details: {response_json["detail"]}')
            return False


async def get_stages_tutor(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'stages_tutor/stages'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_stages_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stages_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def get_stages_agreement_tutor(link:str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'agreement/get_list'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_stages_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stages_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def approve_agreement_tutor(order_number: int, link: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}agreement/approve/{order_number}'
        headers = await get_headers(link)
        async with session.put(url, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} approve_agreement_tutor status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} approve_agreement_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def get_stages_prepayment_tutor(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'prepayment/get_list'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_stages_prepayment_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stages_prepayment_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def approve_prepayment_tutor(order_number: int, link: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}prepayment/approve/{order_number}'
        headers = await get_headers(link)
        async with session.put(url, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} approve_prepayment_tutor status OK (200)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} approve_prepayment_tutor status {response.status}, details: {response_json["detail"]}')
            return False


async def get_stages_outlay_tutor(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'outlay_record/get_list'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_stages_outlay_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stages_outlay_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def approve_outlay_tutor(order_number: int, link: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}outlay_record/approve/{order_number}'
        headers = await get_headers(link)
        async with session.put(url, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} approve_outlay_tutor status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} approve_outlay_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def get_stages_report_tutor(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'report/get_list'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {str(link)} get_stages_report_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} get_stages_report_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def approve_report_tutor(order_number: int, link: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}report/approve/{order_number}'
        headers = await get_headers(link)
        async with session.put(url, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {str(link)} approve_report_tutor status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {str(link)} approve_report_tutor status {response.status}, details: {response_json["detail"]}')
            return False

async def make_penalty_tutor(data: dict, link: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}penalty/create'
        headers = await get_headers(link)
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 201:
                logger.info(f'user {link} make_penalty_tutor status OK (201)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} make_penalty_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def get_penalty_tutor(engineers_number:int,link: str):
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}penalty/tutor/{engineers_number}'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {link} get_penalty_tutor status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {link} get_penalty_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def get_penalty_engineer(link: str):
    async with aiohttp.ClientSession() as session:
        url = base_url + 'penalty/engineer'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {link} get_penalty_engineer status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(f'user {link} get_penalty_engineer status {response.status} details: {response_json["detail"]}')
            return False

async def delete_agreement_tutor(order_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}agreement/delete/{order_number}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {link} delete_agreement_tutor status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(f'user {link} delete_agreement_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def delete_prepayment_tutor(order_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}prepayment/delete/{order_number}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {link} delete_prepayment_tutor status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {link} delete_prepayment_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def delete_outlays_tutor(order_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}outlay_record/delete/{order_number}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {link} delete_outlays_tutor status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {link} delete_outlays_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def delete_report_tutor(order_number:int, link:str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}report/delete/{order_number}'
        headers = await get_headers(link)
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                logger.info(f'user {link} delete_report_tutor status OK (204)')
                return True
            response_json = await response.json()
            logger.warn(
                f'user {link} delete_report_tutor status {response.status} details: {response_json["detail"]}')
            return False

async def get_photo(order_number:int, link:str):
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}report/get/photo/{order_number}'
        headers = await get_headers(link)
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info(f'user {link} get_photo status OK (200)')
                return await response.json()
            response_json = await response.json()
            logger.warn(
                f'user {link} get_photo status {response.status} details: {response_json["detail"]}')
            return False

async def download_photo(photo_url: str, filename: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as response:
            if response.status == 200:
                async with aiofiles.open(filename, mode='wb') as file:
                    logger.info(f'download_photo status OK (200)')
                    await file.write(await response.read())
                return True
            response_json = await response.json()
            logger.warn(
                f'download_photo status {response.status} details: {response_json["detail"]}')
            return False