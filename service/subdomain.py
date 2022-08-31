from asyncio import Task
import os
import sys
from extensions import db
from models import DomainModels, TaskModels

def startSubdomainTask(domain, task_id):
    '''Start a new subdomain task'''
    TaskModels.query.filter_by(task_id=task_id).update({'task_running_module': 'Subdomain'})
    db.session.commit()
    try:
        os.system()
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return fail_api('暂停失败')

