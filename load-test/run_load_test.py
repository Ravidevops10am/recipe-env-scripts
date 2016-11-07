#!

import getopt, sys, time, requests, random, string
from threading import Thread


class SingleUser(Thread):

    def __init__(self, thread_id, web_ip):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.web_ip = web_ip
        self.base_url = 'http://' + web_ip + ':8000'

    def run(self):
        while(True):
            self.runSingleUserForever()

    def random_string(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length))


    def user_name_length(self):
        return random.randint(5, 15)


    def recipe_name_length(self):
        return random.randint(15, 50)


    def recipe_content_length(self):
        return random.randint(200, 1000)


    def email_length(self):
        return random.randint(20, 35)


    def random_seconds(self, low, high):
        return random.uniform(low, high)


    def random_user_id(self, users):
        try:
            return random.choice(users)
        except:
            return ''


    def random_recipe(self, recipes):
        try:
            return random.choice(recipes)
        except:
            return ''


    def random_user_email(self, emails):
        try:
            return random.choice(emails)
        except:
            return ''


    def append_user(self, user, users):
        if user is None:
            return
        users.append(user)


    def append_recipe(self, recipe, recipes):
        if recipe is None:
            return
        recipes.append(recipe)


    def header(self, user_id=None):
        if user_id is None:
            return {'Content-Type': 'application/json'}
        else:
            return {'Content-Type': 'application/json', 'RequestingUser': user_id}


    def getRecipeList(self, user_id):
        try:
            print('Thread ' + str(self.thread_id) + ': GET Recipe List')
            requests.get(self.base_url + '/api/recipe', headers=self.header(user_id=user_id))
        except:
            return


    def getUserRecipeBook(self, user_id):
        try:
            print('Thread ' + str(self.thread_id) + ': GET Recipe Book')
            requests.get(self.base_url + '/api/user/' + user_id + '/recipe-book', headers=self.header(user_id=user_id))
        except:
            return


    def getUserByEmail(self, email):
        try:
            print('Thread ' + str(self.thread_id) + ': GET User by email')
            requests.get(self.base_url + '/api/user?email=' + email, headers=self.header())
        except:
            return


    def postUser(self, users, emails):
        try:
            print('Thread ' + str(self.thread_id) + ': POST User')
            post_data = {"userName": self.random_string(self.user_name_length()), "userEmail": self.random_string(self.email_length())}
            response = requests.post(self.base_url + '/api/user', json=post_data, headers=self.header())
            users.append(response.json()['userId'])
            emails.append(response.json()['userEmail'])
        except:
            return


    def postRecipe(self, user_id, recipes):
        try:
            print('Thread ' + str(self.thread_id) + ': POST Recipe')
            post_data = {"recipeName": self.random_string(self.recipe_name_length()), "recipeContent": self.random_string(self.recipe_content_length())}
            response = requests.post(self.base_url + '/api/recipe', json=post_data, headers=self.header(user_id=user_id))
            recipes.append(response.json()['recipeId'])
        except:
            return


    def putRecipe(self, recipe_id, user_id):
        try:
            print('Thread ' + str(self.thread_id) + ': PUT Recipe')
            put_data = {"recipeName": self.random_string(self.recipe_name_length()), "recipeContent": self.random_string(self.recipe_content_length())}
            requests.put(self.base_url + '/api/recipe/' + recipe_id, json=put_data, headers=self.header(user_id=user_id))
        except:
            return


    def getRecipe(self, recipe_id, user_id):
        try:
            print('Thread ' + str(self.thread_id) + ': GET Recipe')
            requests.get(self.base_url + '/api/recipe/' + recipe_id, headers=self.header(user_id=user_id))
        except:
            return


    def getUserById(self, user_id):
        try:
            print('Thread ' + str(self.thread_id) + ': GET User')
            requests.get(self.base_url + '/api/user/' + user_id, headers=self.header())
        except:
            return


    def postUserRecipeBook(self, user_id, recipe_id):
        try:
            print('Thread ' + str(self.thread_id) + ': POST to Recipe Book')
            post_data = {"recipe_id": recipe_id}
            requests.post(self.base_url + '/api/user/' + user_id + '/recipe-book', json=post_data, headers=self.header(user_id=user_id))
        except:
            return


    def deleteRecipeFromRecipeBook(self, user_id, recipe_id):
        try:
            print('Thread ' + str(self.thread_id) + ': DELETE from Recipe Book')
            requests.delete(self.base_url + '/api/user/' + user_id + '/recipe-book/' + recipe_id, headers=self.header(user_id=user_id))
        except:
            return


    def runSingleUserForever(self):
        users = []
        recipes = []
        emails = []

        self.postUser(users, emails)
        time.sleep(self.random_seconds(2, 5))

        self.getRecipeList(user_id=None)
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 6))

        self.getRecipeList(self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 6))

        self.getUserByEmail(self.random_user_email(emails))
        time.sleep(self.random_seconds(1, 3))

        self.postUser(users, emails)
        time.sleep(self.random_seconds(1, 3))

        self.postRecipe(self.random_user_id(users), recipes)
        self.getRecipe(self.random_recipe(recipes), self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(10, 18))

        self.postRecipe(self.random_user_id(users), recipes)
        self.getRecipe(self.random_recipe(recipes), self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(10, 18))

        self.getUserById(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 6))

        self.getRecipeList(self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 4))

        self.postUserRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 3))

        self.postUserRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 3))

        self.postUserRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 4))

        self.getRecipeList(self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 5))

        self.getRecipe(self.random_recipe(recipes), self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 3))

        self.getRecipeList(self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(6, 10))

        self.getUserById(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 4))

        self.deleteRecipeFromRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 3))

        self.getUserById(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 5))

        self.deleteRecipeFromRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(3, 6))

        self.getRecipe(self.random_recipe(recipes), self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 3))

        self.deleteRecipeFromRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 2))

        self.postUserRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(3, 7))

        self.getUserByEmail('asdfasdf')
        time.sleep(self.random_seconds(3, 7))

        self.getUserById(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 4))

        self.getRecipe(self.random_recipe(recipes), self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(3, 7))

        self.putRecipe(self.random_recipe(recipes), self.random_user_id(users))
        time.sleep(self.random_seconds(1, 4))

        self.getUserById(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 4))

        self.getRecipe(self.random_recipe(recipes), self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(3, 7))

        self.deleteRecipeFromRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 2))

        self.postUserRecipeBook(self.random_user_id(users), self.random_recipe(recipes))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 4))

        self.getUserById(self.random_user_id(users))
        self.getRecipeList(self.random_user_id(users))
        time.sleep(self.random_seconds(1, 3))

        self.getRecipeList(self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 4))

        self.getRecipeList(self.random_user_id(users))
        self.getUserRecipeBook(self.random_user_id(users))
        time.sleep(self.random_seconds(2, 4))



if __name__ == "__main__":
    num_users = int(sys.argv[1])
    web_ip = str(sys.argv[2])
    time_between_new_users = int(sys.argv[3])
    print('Running Test against ' + web_ip + ' with ' + str(num_users) + ' user thread(s), with a new user starting approximately every ' + str(time_between_new_users) + ' seconds.')

    userThreads = []
    for i in range(num_users):
        simulated_user = SingleUser(i, web_ip)
        userThreads.append(simulated_user)
        simulated_user.start()
        time.sleep(time_between_new_users)

    for userThread in userThreads:
        userThread.join()

    print('Done running tests')

