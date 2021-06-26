"""MongoDB Helper Class"""
import pymongo

CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
DATABASE_ENTRIES = CLIENT["NLPUserAction"]['entries']
DATABASE_TESTCASE = CLIENT["NLPUserAction"]['testcase']


class MongoHelper:
    """Definition of Class MongoHelper"""

    @staticmethod
    def get_all_objects(condition=None):
        """ Returns database searches"""
        return [x for x in DATABASE_ENTRIES.find({}, {'_id': 0})] if condition is None else \
            [x for x in DATABASE_ENTRIES.find(condition, {'_id': 0})]

    @staticmethod
    def add_object(value):
        """ Adds value into database """
        return DATABASE_ENTRIES.insert(value)

    @staticmethod
    def add_objects(values):
        """ Adds values into database """
        return DATABASE_ENTRIES.insert_many(values)

    @staticmethod
    def insert_if_not_exist(value):
        """ Adds value into database if not present """
        dblist = CLIENT.list_database_names()
        return DATABASE_ENTRIES.update(value, value, upsert=True) if "mydatabase" in dblist else MongoHelper.add_object(
            value)


class TestCaseHelper:
    """Definition of Class TestCaseHelper"""

    def get_testcase_id_of(testcase_type):
        """ Finds the testcase id of the specific test case from the database """
        if DATABASE_TESTCASE.count_documents({'case_type': testcase_type}) > 0:
            current_count = DATABASE_TESTCASE.find(
                {'case_type': testcase_type}, {'_id': 0})[0]['count'] + 1
            DATABASE_TESTCASE.update_one({"case_type": testcase_type}, {
                                         "$set": {'count': current_count}})
            return current_count
        else:
            DATABASE_TESTCASE.insert({'case_type': testcase_type, 'count': 0})
            return 0

    def get_testcase_id(testcase_type):
        """ Returns the testcase id of the specific test case """
        return f"TC{testcase_type}0{TestCaseHelper.get_testcase_id_of(testcase_type)}"
