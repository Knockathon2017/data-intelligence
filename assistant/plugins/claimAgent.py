from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

import numpy as np
from pymongo import MongoClient
CLIENT = MongoClient('localhost',27017)
db = CLIENT['ExzeoSmartUnderWriting']
claim_config_coll = 'claim_config'
zip_config_coll = 'zip_config'
image_config_coll = 'image_meta'
questions_config_coll = 'question_meta'
claim_config = db[claim_config_coll].find_one()
zip_config = db[zip_config_coll].find_one()
image_configs = [res for res in db[image_config_coll].find()]
questions =  [res for res in db[questions_config_coll].find()]
image_config = {}
for image_meta in image_configs:
	if image_meta['_id'] not in image_config:
		image_config[image_meta['_id']] = image_meta

class ClaimAgentPlugin(WillPlugin):
	def __init__(self):
		self.zip_code = 0
		self.sqr_feet_area = 0
		self.pet_count = 0
		self.previous_claim_count = 0
		self.trampoline_present = 0
		self.pool_present = 0
		self.crime = 0
		self.dist_coast = 0
		self.score = 0
		# self.breed_name = ''
		# self.blacklisted_breeds = ["american pit bull terrier","rottweiler","german shepherd"]

	def set_zip_code(self, zip_code):
		self.zip_code = zip_code
	
	def set_sqr_feet_area(self, sqr_feet_area):
		self.sqr_feet_area = sqr_feet_area
	
	def set_pet_count(self, pet_count):
		self.pet_count = pet_count
	
	def	set_previous_claim_count(self, previous_claim_count):
		self.previous_claim_count = previous_claim_count
	
	def set_trampoline(self, trampoline_present):
		self.trampoline_present = trampoline_present
	
	def set_pool(self, pool_present):
		self.pool_present = pool_present
	
	@hear("\s?want an insurance policy")
	def start_claim_conversation(self, message):
		self.reply(message, "Ok, let's get started with the process")
		self.reply(message, "Believe me it's very easy!")
		self.reply(message, "May I Know the zip code where you stay?")

	@respond_to("\s?Zip\s? (?P<zip_code>\d+)")
	def get_zip_code(self, message, zip_code):
		self.set_zip_code(zip_code)
		self.reply(message,"May I also know Square Feet area of your house?")
	
	@respond_to("\s?Square Feet Area\s? (?P<sqr_feet_area>\d+)")
	def get_sqr_feet_area(self, message, sqr_feet_area):
		self.set_sqr_feet_area(float(sqr_feet_area))
		self.reply(message,"Also, need Pets and Number of previous claims you have filed")
	
	@respond_to("\s?Pets\s? (?P<pet_count>\d+)")
	def get_pet_count(self, message, pet_count):
		self.set_pet_count(float(pet_count))
		self.reply(message,"Got It!")
		self.reply(message,"Also number of previous claims you have filed!")
		# if self.zip_code.endswith("15"):
		# 	if self.pet_count > 0:
		# 		self.reply(message,"Dangerous dog breeds reside in your area")
		# 		self.reply(message,"Titan wants to know which breed of dog you own?")

	@respond_to("\s?Previous claims\s? (?P<previous_claim_count>\d+)")
	def get_previous_claim_count(self, message, previous_claim_count):
		self.set_previous_claim_count(float(previous_claim_count))
		self.reply(message,"Thanks for being so patient till now!")
		self.reply(message,"Titan would also like to know whether you have trampoline in your premises and also the pool?")
	
	@respond_to("\s?Trampoline\s? (?P<trampoline_present>[a-zA-Z]+)")
	def get_trampoline(self, message, trampoline_present):
		if trampoline_present.lower() in ['yes', 'yo', 'yep' ,'of course']:
			tp = 1
		elif trampoline_present.lower() in ['no', 'nep','nehh','not at all']:
			tp = 0
		else:
			tp = float(trampoline_present)
		self.set_trampoline(tp)
		self.reply(message,"Thanks!")
		self.reply(message,"Is there any pool?")
	
	@respond_to("\s?Pool\s? (?P<pool_present>[a-zA-Z]+)")
	def get_pool(self, message, pool_present):
		if pool_present.lower() in ['yes', 'yo', 'yep','of course','yess']:
			p = 1
		elif pool_present.lower() in ['no', 'nep','nehh','not at all']:
			p = 0
		else:
			p = float(pool_present)
		self.set_pool(p)
		self.reply(message,"Thank you very much for believing in Titan!")
		self.reply(message,"Let me crunch the data and analyse your property and its surrounding..")
		self.claim_file_process(message,
								self.zip_code,
								self.sqr_feet_area,
								self.pet_count,
								self.previous_claim_count,
								self.trampoline_present,
								self.pool_present)

	@respond_to("\s?uploaded\s? (?P<image_id>[0-9a-zA-Z]+)")
	def get_image_upload_status(self, message, image_id):
		if image_id in image_config:
			image_meta_info = image_config[image_id]
			no_of_elements_in_image = len(image_meta_info)-1
			self.reply(message,"Found %s things as part of your interiors %s"%(no_of_elements_in_image,image_id))
			self.reply(message,"Found:")
			prev_score = self.score
			for k,v in image_meta_info.iteritems():
				if k != '_id':
					self.reply(message,k.capitalize())
					if (k.lower() == 'stove' or k.lower() == 'refrigerator'):
						self.score += 10
			if self.score > prev_score:
				self.reply(message,"Sadly, Risk has increased :(")
				self.reply(message,"Let me check whether we can still proceed!")
		else:
			self.reply(message,"Unable to find anything from image, Titan needs to learn some more deep learning stuff!")
		self.evaluate_score(message,self.score,1)

	# @respond_to("\s?breed\s? (?P<breed_name>[a-zA-Z]+)")
	# def set_dog_breed(self, message, breed_name):
	# 	if breed_name.lower() in self.blacklisted_breeds:
	# 		self.breed_name = breed_name

	def claim_file_process(self, message, zip, sqr_feet_area, pet_count, previous_claim_count, trampoline_present, pool_present):
		# print claim_config
		# print zip_config
		# self.reply(message,str(zip))
		# self.reply(message,str(sqr_feet_area))
		# self.reply(message,str(pet_count))
		# self.reply(message,str(previous_claim_count))
		# self.reply(message,str(trampoline_present))
		# self.reply(message,str(pool_present))
		if not zip:
			self.reply(message,"Please provide a valid zip")
		# elif not(zip and sqr_feet_area and pet_count and previous_claim_count and trampoline_present and pool_present):
		# 	self.reply(message,"Please provide complete information")
		# 	self.reply(message,"Only then I'll be able to help you out")
		else:
			score = self.calculate_score(message, zip, sqr_feet_area, pet_count, previous_claim_count, trampoline_present, pool_present)
			self.score = score
			self.reply(message,"We rate this property %s Risk score"%str(score))
			self.evaluate_score(message,self.score)

	def calculate_score(self, message, zip_code, sqr_feet_area, pet_count, previous_claim_count, trampoline_present, pool_present):
		crime = 0
		dist_coast = 0
		if zip_code in zip_config:
			zip_meta = zip_config[zip_code]
			crime = zip_meta['Crime']
			dist_coast = zip_meta['Distance To Coast']
		else:
			self.reply(message,"Currently we do not work in this area")
		conts_row = [sqr_feet_area,crime,dist_coast]
		categs_row = [pet_count, trampoline_present, pool_present,previous_claim_count]
		conts = ['Square Feet Area','Crime','Distance To Coast']
		categs = ['Pets','Trampoline Present','Pool Present','Previous Claims'] 
		score = 0
		for i,each in enumerate(conts):
			v = claim_config[each]
			index = np.digitize(conts_row[i],v['Range'])
			sc = v['Score'][index]
			score += sc
		# self.reply(message,"Score" + ' : ' + str(score))
		for i,each in enumerate(categs):
			v = claim_config[each]
			# self.reply(message,str(int(categs_row[i]))+'_'+str(each))
			index = int(v['Range'][int(categs_row[i])])
			sc = v['Score'][index]
			score += sc
		# if self.breed_name:
		# 	score += 20
		self.reply(message,"Titan found that on a scale of 1000, Crime Risk in your area is %s" %str(crime))
		self.reply(message,"Titan also got to know that Average Distance to Coast of your area is %s "%str(dist_coast))
		self.reply(message,"Titan is a lazy learner! :P")
		return score

	def evaluate_score(self, message, score, marker=0):
		if score > 50:
			self.reply(message,"Thanks for being patient up till now!")
			self.reply(message, "Sorry, risk with your property looks too high, Titan has to ask his boss for approval. Hope you understand :(")
		elif score > 30 and score <= 50:
			# moderate risk
			# ask to input images
			self.reply(message,"Your property looks somewhat reachable to us..")
			self.reply(message,"We are almost there ...")
			if marker == 1:
				self.reply(message,"Titan is still not conveinced :(")
				self.reply(message,"It will be great if you can upload another picture of your household")
			else:
				self.reply(message,"But, just before that, Titan would also like to check interiors of your household as well!")
				self.reply(message,"It will be great if you can upload a picture of your drawing room/living room")
		elif score <= 30:
			# very low risk
			# only ask for some extra questions
			# first_question = questions[0]
			# for k,v in first_question:
			# 	if k != '_id':
			# 		self.reply(message,k)
			self.reply(message,"Titan would be happy to tell you that his insurance company is ready to issue you a policy")
			self.reply(message,"Titan will take some extra time to give you a quote ...")
			self.reply(message,"Congratulations!")
			if score <= 10:
				self.reply(message, "Titan says, Least Risk least premiums, Hola!")
				self.reply(message,"You owe a premium of USD500 which can be adjusted monthly or annually.")
			elif score > 10 and score <= 20:
				self.reply(message, "Titan says, Lower Risk lower premiums, Hola!")
				self.reply(message,"You owe a premium of USD1500 which can be adjusted monthly or annually.")
			elif score > 20 and score <= 30:
				self.reply(message, "Titan says, Low Risk low premiums")
				self.reply(message,"You owe a premium of USD2500 which can be adjusted monthly or annually.")
			self.reply(message,"Titan would definitely like to be in touch")
			self.reply(message,"Ping Titan back!")
			self.reply(message,"Someone from Titan's company will visit soon")
			
# if __name__ == '__main__':
# 	ClaimAgentPlugin().claim_file_process()