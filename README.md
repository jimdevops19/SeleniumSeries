# Updated booking.com bot

Jim from [JimShapedCoding](https://www.youtube.com/channel/UCU8d7rcShA7MGuDyYH1aWGg)
made this bot as an example for his Selenium tutorials. The bot no longer works,
so I decided to fork and update it. I'm by no means an expert, 
but fairly happy with the code - hopefully someone will find it useful.

* [Updated booking.com bot](#updated-bookingcom-bot)
* [Issues and limitations](#issues-and-limitations)
* [Major changes](#major-changes)
* [Improvements](#improvements)
* [See also](#see-also)
<!-- TOC -->

## Issues and limitations

I skipped selecting currency and selecting the number of people altogether.
Booking.com seems to have some terrible, unstable locators - not sure if it
was better two years ago, but now some elements seem impossible to navigate
without sacrificing readability. I might give it another try with
CSS selectors once I have more experience with them.

The bot works around 7-8/10 times - the "*Where are you going?*" and
"*check-in - check-out*" dropdowns still misbehave sometimes. I suppose
Selenium actions could fix that.

## Major changes

1. Uses Selenium 4! 
1. No inputs. A descriptive Python config file with some extra settings instead
   (`booking/config.py`)
1. Explicit, conditional, configurable waits
1. Most Jim's locators no longer worked, so I used different ones - mostly
   xpath if By.ID and By.NAME failed
1. I used [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager).
   No need to download chrome drivers manually!


## Improvements

1. A method for accepting cookies
1. Simplified and moved methods from `Filtration.py` and `Raport.py`
1. Conditional waits in `select_place_to_go()` prevent the driver
   from accidentally choosing from "*Popular destinations nearby*"
1. The bot can now handle problematic deals marked as "*New to booking.com*"
   (with not enough ratings)
1. Star rating checkboxes are "scrolled to" with JavaScript to avoid errors
1. Proper `requirements.txt`
1. A relative locator for the first location/place to go result
1. An extra `highligh_element()` function in `booking/js_utils.py`. I recommend
   using it when testing or debugging.


## See also

* Jim's tutorial was also feetured on [FreeCodeCamp's YT channel](https://www.youtube.com/watch?v=j7VZsCCnptM&t=4603s)
