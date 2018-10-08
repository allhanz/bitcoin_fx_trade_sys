
#=========================================================


#==========================================================

######  reinforcement_learning.py  ###########
#reinforcement learning model
#website:https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow
#a chinese guy talk about
#sarsa algorithm 

#=========================================================

######### webdriver_wait.py ###########
import os
import sys
import selenium.webdriver.support.ui.WebDriverWait as WebDriverWait


def find_elements(driver, elem_path, by=CSS, timeout=TIMEOUT, poll_frequency=0.5):
        """ Find and return all elements once located

        find_elements locates all elements on the page, waiting
        for up to timeout seconds. The elements, when located,
        are returned. If not located, a TimeoutException is raised.

        Args:
                driver (selenium webdriver or element): A driver or element
                elem_path (str): String used to located the element
                by (selenium By): Selenium By reference
                timeout (int): Selenium Wait timeout, in seconds
                poll_frequency (float): Selenium Wait polling frequency, in seconds

        Returns:
                list of elements: Selenium element

        Raises:
                TimeoutException: Raised when target element isn't located
        """
        wait = WebDriverWait(driver, timeout, poll_frequency)
        return wait.until(EC.presence_of_all_elements_located((by, elem_path))) 
#==========================================