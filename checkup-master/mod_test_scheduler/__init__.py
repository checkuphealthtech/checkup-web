import importlib

class TestScheduler(object):
    def __init__(self):
        pass
    
    # def get_schedule_action_profile(self, external_order_id=None, internal_order_id=None):
    def get_schedule_action_profile(self, external_order_id=None, internal_order_id=None):
        profiles_module = __import__("mod_data_receiver.profiles")
        profile_instance = getattr(profiles_module,self.provider)
        profile_instance = profile_instance()
        # create a global object containging our module
        # globals()[self.provider] = retrieve_profile
        return profile_instance

    def schedule_test_for(self, profile, user_email, data):
        # the_profile = self.get_schedule_action_profile(profile)
        profiles_module = __import__("mod_test_scheduler.profiles", fromlist=[profile])
        profile_instance = getattr(profiles_module, profile)
        profile_instance = profile_instance()
        results = profile_instance.submit(data)
        if results == True:
            # save pending in database
            return True
        else:
            return False