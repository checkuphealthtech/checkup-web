import importlib
import uuid

class DataReceiverTask(object):
    RETRIEVE = "RETRIEVE"
    TRANSFORM_AND_SAVE = "TRANSFORM_AND_SAVE"
    def __init__(self, provider, action, lab_test_id, test_name=None):
        self._id = None
        self.provider = provider
        self.lab_test_id = lab_test_id
        self.action = action
        self.test_name = test_name
        if self._id == None:
            self.setup_id()
    
    def get_profile(self):
        profiles_module = __import__("mod_data_receiver.profiles", fromlist=[self.profile])
        profile_instance = getattr(profiles_module, self.provider)
        profile_instance = profile_instance(self)
        # create a global object containging our module
        # globals()[self.provider] = retrieve_profile
        return profile_instance
    def do(self):
        profiles_module = __import__("mod_data_receiver.profiles", fromlist=[self.provider])
        the_profile = getattr(profiles_module, self.provider)
        profile_instance = the_profile(self)

        if self.action == self.RETRIEVE:
            profile_instance.retrieve()
        elif self.action == self.TRANSFORM_AND_SAVE:
            profile_instance.transform_and_save()
        else:
            pass

    def get_task_dict(self):
    	return vars(self)

    def setup_id(self):
        self._id = str(uuid.uuid4())