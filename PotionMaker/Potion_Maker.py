import time
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from model.runelite_bot import BotStatus
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from utilities.geometry import RuneLiteObject
import pyautogui as pag
import model.osrs.PotionMaker.BotSpecImageSearch as imsearch
import utilities.game_launcher as launcher
import pathlib
import model.osrs.PotionMaker.potion_recipes as potion_recipes



    
class OSRSPotionMaker(OSRSBot, launcher.Launchable):
    api_m = MorgHTTPSocket()
    def __init__(self):
        bot_title = "ThatOneGuys Potion Maker"
        description = "This bot makes potions at the bank."
        super().__init__(bot_title=bot_title, description=description)
        self.potion_to_make = None
        self.running_time = 1
        self.take_breaks = False
        self.break_length_min = 1
        self.break_length_max = 500
        self.time_between_actions_min =0.8
        self.time_between_actions_max =5
        self.potion_to_make = None
        self.loop_to_run = None
        self.mouse_speed = "medium"
        self.break_probabilty = 0.13

    def create_options(self):
        self.options_builder.add_dropdown_option("potion_to_make", "Select Potion", potion_recipes.Potion_names)
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])
        self.options_builder.add_slider_option("break_probabilty", "Chance to take breaks (percent)",1,100)
        self.options_builder.add_slider_option("break_length_min", "How long to take breaks (min) (Seconds)?", 1, 300)
        self.options_builder.add_slider_option("break_length_max", "How long to take breaks (max) (Seconds)?", 2, 300)    
        self.options_builder.add_checkbox_option("mouse_speed", "Mouse Speed (must choose & only select one)",[ "slowest", "slow","medium","fast","fastest"])
        self.options_builder.add_slider_option("time_between_actions_min", "How long to take between actions (min) (MiliSeconds)?", 600,3000)
        self.options_builder.add_slider_option("time_between_actions_max", "How long to take between actions (max) (MiliSeconds)?", 600,3000)
        
                                               
    def save_options(self, options: dict):
        for option in options:
            if  option == "potion_to_make":
                self.potion_to_make = options[option]         
            elif option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            elif option == "break_length_min":
                self.break_length_min = options[option]
            elif option == "break_length_max":
                self.break_length_max = (options[option])
            elif option == "mouse_speed":
                self.mouse_speed = options[option]
            elif option == "time_between_actions_min":
                self.time_between_actions_min = options[option]/1000
            elif option == "time_between_actions_max":
                self.time_between_actions_max = options[option]/1000
            elif option == "break_probabilty":
                self.break_probabilty = options[option]/100
                
                
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg(f"We are making {self.potion_to_make}s")
        self.log_msg("Options set successfully.")
        self.options_set = True


    def launch_game(self):
        settings = pathlib.Path(__file__).parent.joinpath("custom_settings.properties")
        launcher.launch_runelite_with_settings(self, settings)

    def main_loop(self):
        start_time = time.time()
        end_time = self.running_time * 60
        print(self.mouse_speed)
        self.setup()
     
        print(self.loop_to_run)
        
    
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            # 5% chance to take a break between tree searches
            if rd.random_chance(probability=self.break_probabilty) and self.take_breaks:
                self.take_break(min_seconds =self.break_length_min, max_seconds=self.break_length_max, fancy=True)   
            if self.loop_to_run == 1:
                self.update_progress((time.time() - start_time) / end_time)
                self.bot_loop_stackable()
            elif self.loop_to_run == 2:
                self.update_progress((time.time() - start_time) / end_time)
                self.bot_loop_super_combat()
            elif self.loop_to_run == 3:
                self.update_progress((time.time() - start_time) / end_time)
                self.bot_loop_main()
        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()
         
            
    def bot_loop_stackable(self):
        
        self.withdrawl_ingrediants(self.potion_to_make)        
        self.close_bank()
        self.mix_ingredients(self.potion_to_make)       
        self.make_all()
        self.check_inv()
        self.find_nearest_bank()
        self.deposit_items() 
            
    def bot_loop_super_combat(self):
        
        self.withdrawl_ingrediants_super_combat(self.potion_to_make)     
        self.close_bank()
        self.mix_ingredients(self.potion_to_make)       
        self.make_all()
        self.check_inv()
        self.find_nearest_bank()
        self.deposit_items()
               
    def bot_loop_main(self):
        print("made it to main loop")
      
        self.withdrawl_ingrediants(self.potion_to_make)           
        self.close_bank()
        self.mix_ingredients(self.potion_to_make)       
        self.make_all()
        self.check_inv()
        self.find_nearest_bank()
        self.deposit_items()
                         
    def find_nearest_bank(self):
          
        if banks := self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN):
            banks = sorted(banks, key=RuneLiteObject.distance_from_rect_center)
            self.log_msg(f"Bank found")               
            self.mouse.move_to(banks[0].random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            
            
        else:
            self.log_msg(f"aay you moron stand near a bank tagged cyan")       
            
    def deposit_items(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "deposit.png")
        
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
           
        self.log_msg(f"depositing all items")
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])
        self.mouse.click()
        time.sleep(Sleep_time)

    def open_up_potions_tab(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Potions_tab_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "PotionsTab.png")
        
        if potions_tab := imsearch.search_img_in_rect(Potions_tab_img, self.win.game_view):
            self.log_msg(f"clicking potions tab")
            self.mouse.move_to(potions_tab.random_point())
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"aaay you idiot there no potion tab")
                  
    def open_inventory(self):
        self.log_msg("Selecting inventory...")
        self.mouse.move_to(self.win.cp_tabs[3].random_point(),mouseSpeed=self.mouse_speed[0])
        self.mouse.click()
   
    def set_supplies_amount(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        sleep_time_key = rd.fancy_normal_sample(0.067, 0.084)
        sleep_time_between_key = rd.fancy_normal_sample(0.156, 0.248)   
        withdrawl_x_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "withdrawl_x.png")
        withdrawl_x_clicked_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "withdrawl_x_clicked.png")
        withdrawl_all_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "withdrawl_all.png")
        withdrawl_all_clicked_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "withdrawl_all_clicked.png")
        keywords = ["Divine","Stamina","Extended","Ancient Brew","Forgotten Brew"]
        keywords2 = ["Super Combat"]
        Pot_to_make = f"{self.potion_to_make}"
       
        
        found_keyword = False
        found_keyword2 = False
        for keyword in keywords:
            if keyword in Pot_to_make:
                found_keyword = True
                break   
        if found_keyword:
            if withdrawl_all:= imsearch.search_img_in_rect(withdrawl_all_img, self.win.game_view):
                self.mouse.move_to(withdrawl_all.random_point(),mouseSpeed=self.mouse_speed[0])
                self.mouse.click
                time.sleep(Sleep_time)
            elif withdrawl_all_clicked := imsearch.search_img_in_rect(withdrawl_all_clicked_img, self.win.game_view):
                 time.sleep(Sleep_time)
            else:
                self.log_msg(f"Could not set withdrawl amount")
                self.log_msg("Finished.")
                self.stop()
                    
        elif found_keyword2:
            for keyword in keywords2:
                if keyword in Pot_to_make:
                    found_keyword2 = True
                    break
            if found_keyword2:
                if Withdrawl_x := imsearch.search_img_in_rect(withdrawl_x_img, self.win.game_view):
                    self.log_msg(f"Setting withdrawl amount")
                    self.mouse.move_to(Withdrawl_x.random_point(),mouseSpeed=self.mouse_speed[0])
                    time.sleep(Sleep_time)
                    self.mouse.right_click()
                    time.sleep(Sleep_time)  
                    self.mouse.move_rel(0,40)
                    self.mouse.click()
                    time.sleep(Sleep_time)
                    pag.keyDown('7')
                    time.sleep(sleep_time_key)
                    pag.keyUp('7')
                    time.sleep(sleep_time_between_key)  
                elif Withdrawl_x := imsearch.search_img_in_rect(withdrawl_x_clicked_img, self.win.game_view):
                    self.log_msg(f"Setting withdrawl amount")
                    self.mouse.move_to(Withdrawl_x.random_point(),mouseSpeed=self.mouse_speed[0])
                    self.mouse.click()
                    time.sleep(Sleep_time)
                    self.mouse.right_click()
                    time.sleep(0.2)  
                    self.mouse.move_rel(0,40)
                    time.sleep(Sleep_time)
                    self.mouse.click()
                    time.sleep(Sleep_time)
                    pag.keyDown('7')
                    time.sleep(sleep_time_key)
                    pag.keyUp('7')
                    time.sleep(sleep_time_between_key)
                else:
                    self.log_msg(f"Could not set withdrawl amount")
                    self.log_msg("Finished.")
                    self.stop()      
        else: 
            
            if Withdrawl_x := imsearch.search_img_in_rect(withdrawl_x_img, self.win.game_view):
                self.log_msg(f"Setting withdrawl amount")
                self.mouse.move_to(Withdrawl_x.random_point(),mouseSpeed=self.mouse_speed[0])
                time.sleep(Sleep_time)
                self.mouse.right_click()
                time.sleep(Sleep_time)  
                self.mouse.move_rel(0,40)
                self.mouse.click()
                pag.keyDown('1')
                time.sleep(sleep_time_key)
                pag.keyUp('1')
                time.sleep(sleep_time_between_key)
                pag.keyDown('4')
                time.sleep(sleep_time_key)
                pag.keyUp('4')
                time.sleep(sleep_time_between_key)
                pag.keyDown('enter')
                time.sleep(sleep_time_key)
                pag.keyUp('enter')
                time.sleep(sleep_time_between_key)
            
            elif Withdrawl_x := imsearch.search_img_in_rect(withdrawl_x_clicked_img, self.win.game_view):
                
                self.log_msg(f"Setting withdrawl amount")
                self.mouse.move_to(Withdrawl_x.random_point(),mouseSpeed=self.mouse_speed[0])
                self.mouse.click()
                time.sleep(sleep_time_between_key)
                self.mouse.right_click()
                time.sleep(0.2)  
                self.mouse.move_rel(0,40)
                time.sleep(Sleep_time)
                self.mouse.click()
                time.sleep(Sleep_time)
                pag.keyDown('1')
                time.sleep(sleep_time_key)
                pag.keyUp('1')
                time.sleep(sleep_time_between_key)
                pag.keyDown('4')
                time.sleep(sleep_time_key)
                pag.keyUp('4')
                time.sleep(sleep_time_between_key)
                pag.keyDown('enter')
                time.sleep(sleep_time_key)
                pag.keyUp('enter')
                time.sleep(sleep_time_between_key)
                
            else:
                self.log_msg(f"Could not set withdrawl amount")
                self.log_msg("Finished.")
                self.stop()
                          
    def withdrawl_ingrediants(self, potion_name):
        if potion_name in potion_recipes.potion_recipes:
            ingredients = potion_recipes.potion_recipes[potion_name]
            ingredient1, ingredient2 = ingredients
            print(ingredient1,ingredient2)
        else:
            self.log_msg(f"No recipe found for {potion_name}")
            self.stop()
           


        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Ingrediant_one_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient1)  
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient2)
        if Ingrediant_one := imsearch.search_img_in_rect(Ingrediant_one_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_one.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
                
        if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_two.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
          
    def setup(self):
        keywords = ["Divine","Stamina","Extended","Ancient Brew","Forgotten Brew"]
        keywords2 = ["Super Combat"]
        Pot_to_make = f"{self.potion_to_make}"
        print(Pot_to_make)
        
        found_keyword = False
        found_keyword2 = False
        for keyword in keywords:
            if keyword in Pot_to_make:
                found_keyword = True
                break   
        if found_keyword:
            self.loop_to_run = 1   
            
        elif found_keyword2:
            for keyword in keywords2:
                if keyword in Pot_to_make:
                    found_keyword2 = True
                    break
            if found_keyword2:
                 self.loop_to_run =2
                
        else: 
            self.loop_to_run = 3
   
        self.open_inventory()
        self.find_nearest_bank()
        self.deposit_items()
        self.open_up_potions_tab()
        self.set_supplies_amount()

    def mix_ingredients(self, potion_name):
        if potion_name in potion_recipes.potion_recipes:
            ingredients = potion_recipes.potion_recipes[potion_name]
            ingredient1, ingredient2 = ingredients
        else:
            self.log_msg(f"No recipe found for {potion_name}")
            self.stop()
         

        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Ingrediant_one_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient1)  
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient2)
        if Ingrediant_one := imsearch.search_img_in_rect(Ingrediant_one_img, self.win.control_panel):
            self.mouse.move_to(Ingrediant_one.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
                
        if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.control_panel):
            self.mouse.move_to(Ingrediant_two.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
            
    def close_bank(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Close_Bank_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "x.png")
        
        if Close_bank := imsearch.search_img_in_rect(Close_Bank_img, self.win.game_view):
            self.mouse.move_to(Close_bank.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Could not close bank")
            self.stop()
               
    def make_all(self):
        sleep_time_key = rd.fancy_normal_sample(0.067, 0.084)
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        make_all_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "make_all.png")  
        make_all_not_marked_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "make_all_clicked.png")
        
        if make_all := imsearch.search_img_in_rect(make_all_img, self.win.chat):
            pag.keyDown('space')
            time.sleep(sleep_time_key)
            pag.keyUp('space')
           
        elif make_all := imsearch.search_img_in_rect(make_all_not_marked_img, self.win.chat):
            self.mouse.move_to(make_all.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
            pag.keyDown('space')
            time.sleep(sleep_time_key)
            pag.keyUp('space')
        else:
            self.log_msg(f"Couldn't make all potions")
            self.stop()
                            
    def check_inv(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        emptyslot27_img = imsearch.BOT_IMAGES.joinpath("potion_bot", "inventoryslot27.png")
        counter = 0
        finished = False
        while counter < 60 and not finished:
            while True:
                emptyslot27 = imsearch.search_img_in_rect(emptyslot27_img, self.win.inventory_slots[27])
                if emptyslot27:
                    self.log_msg(f"Finished potions")
                    finished = True
                    break
                self.log_msg(f"waiting to finish potions")
                counter += 1
                time.sleep(1)
        if finished:
            self.log_msg(f"All motions were made")
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"failed to determine if all motions were made")
            self.stop()
    
    def withdrawl_ingrediants_stackable(self,potion_name):
        
        if potion_name in potion_recipes.potion_recipes:
            ingredients = potion_recipes.potion_recipes[potion_name]
            ingredient1, ingredient2 = ingredients
            print(ingredient1,ingredient2)
        else:
            self.log_msg(f"No recipe found for {potion_name}")
            self.stop()
           


        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Ingrediant_one_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient1)  
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient2)
        First_run = False
        if Ingrediant_one := imsearch.search_img_in_rect(Ingrediant_one_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_one.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
        if First_run:      
            if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.game_view):
                self.mouse.move_to(Ingrediant_two.random_point(),mouseSpeed=self.mouse_speed[0])
                self.mouse.click()
                time.sleep(Sleep_time)
                First_run = False
            else:
                self.log_msg(f"Out of ingredients")
                self.stop()
                  
        if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.control_panel):
            time.sleep(0.1)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
            
    def withdrawl_ingrediants_super_combat(self,potion_name):
        
        if potion_name in potion_recipes.potion_recipes:
            ingredients = potion_recipes.potion_recipes[potion_name]
            ingredient1, ingredient2,ingredient3,ingredient4 = ingredients
            print(ingredient1,ingredient2)
        else:
            self.log_msg(f"No recipe found for {potion_name}")
            self.stop()
           


        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Ingrediant_one_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient1)  
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient2)
        Ingrediant_three_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient3)
        Ingrediant_four_img = imsearch.BOT_IMAGES.joinpath("potion_bot", ingredient4)
        
        if Ingrediant_one := imsearch.search_img_in_rect(Ingrediant_one_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_one.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
                
        if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_two.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
            
        if Ingrediant_three := imsearch.search_img_in_rect(Ingrediant_three_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_three.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
        
        if Ingrediant_four := imsearch.search_img_in_rect(Ingrediant_four_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_four.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()