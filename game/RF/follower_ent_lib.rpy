## FOLLOWER EXAMPLE ##

image android_walk_u:
    Transform("RF/example images/android/body/walk/u/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/u/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/u/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/u/3.png",zoom=1.0)
    pause 0.10
    repeat

image android_walk_d:
    Transform("RF/example images/android/body/walk/d/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/d/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/d/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/d/3.png",zoom=1.0)
    pause 0.10
    repeat

image android_walk_h:
    Transform("RF/example images/android/body/walk/h/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/h/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/h/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android/body/walk/h/3.png",zoom=1.0)
    pause 0.10
    repeat

## THIS IS AN EXAMPLE OF A 4 ANGLED IMAGE - ALSO AN EXAMPLE OF OTHER STATES -- used with change_follower_act function ## - use with self.directional_mode = '4' and self.turn = True
default android_lib = {
                    "stand_u": {"image":Transform("RF/example images/android/body/stand/u/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND
                    "stand_h": {"image":Transform("RF/example images/android/body/stand/h/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND
                    "stand_d": {"image":Transform("RF/example images/android/body/stand/d/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND

                    "walk_u": {"image":"android_walk_u", "xoff":-3,"yoff":0}, ## WALK
                    "walk_h": {"image":"android_walk_h", "xoff":-3,"yoff":0}, ## WALK
                    "walk_d": {"image":"android_walk_d", "xoff":-3,"yoff":0}, ## WALK

                    ## OTHER ##
                    "angry": {"image":Transform("RF/example images/android/body/other/angry.png",zoom=1.0), "xoff":-3,"yoff":0}, ## ANGRY
                    "happy": {"image":Transform("RF/example images/android/body/other/happy.png",zoom=1.0), "xoff":-3,"yoff":0}, ## HAPPY
                    "sad": {"image":Transform("RF/example images/android/body/other/sad.png",zoom=1.0), "xoff":-3,"yoff":0}, ## SAD

                }

image android2_walk_u:
    Transform("RF/example images/android2/body/walk/u/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/u/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/u/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/u/3.png",zoom=1.0)
    pause 0.10
    repeat

image android2_walk_d:
    Transform("RF/example images/android2/body/walk/d/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/d/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/d/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/d/3.png",zoom=1.0)
    pause 0.10
    repeat

image android2_walk_hl:
    Transform("RF/example images/android2/body/walk/hl/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/hl/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/hl/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/hl/3.png",zoom=1.0)
    pause 0.10
    repeat

image android2_walk_hr:
    Transform("RF/example images/android2/body/walk/hr/0.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/hr/1.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/hr/2.png",zoom=1.0)
    pause 0.10
    Transform("RF/example images/android2/body/walk/hr/3.png",zoom=1.0)
    pause 0.10
    repeat

## THIS IS AN EXAMPLE OF A 4 ANGLED IMAGE ## - use with self.directional_mode = '4' and self.turn = False
default android2_lib = {
                    "stand_u": {"image":Transform("RF/example images/android2/body/stand/u/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND
                    "stand_hl": {"image":Transform("RF/example images/android2/body/stand/hl/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND
                    "stand_hr": {"image":Transform("RF/example images/android2/body/stand/hr/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND
                    "stand_d": {"image":Transform("RF/example images/android2/body/stand/d/0.png",zoom=1.0), "xoff":-3,"yoff":0}, ## STAND

                    "walk_u": {"image":"android2_walk_u", "xoff":-3,"yoff":0}, ## WALK
                    "walk_hl": {"image":"android2_walk_hl", "xoff":-3,"yoff":0}, ## WALK
                    "walk_hr": {"image":"android2_walk_hr", "xoff":-3,"yoff":0}, ## WALK
                    "walk_d": {"image":"android2_walk_d", "xoff":-3,"yoff":0}, ## WALK

                    ## OTHER ##
                    "angry": {"image":Transform("RF/example images/android2/body/other/angry.png",zoom=1.0), "xoff":-3,"yoff":0}, ## ANGRY
                    "happy": {"image":Transform("RF/example images/android2/body/other/happy.png",zoom=1.0), "xoff":-3,"yoff":0}, ## HAPPY
                    "sad": {"image":Transform("RF/example images/android2/body/other/sad.png",zoom=1.0), "xoff":-3,"yoff":0}, ## SAD

                }
