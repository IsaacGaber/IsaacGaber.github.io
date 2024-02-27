# Isaac John Gaber
import automata, pygame

display_size = (900, 600)

#--------------------------------------------------------
class Gui():
    def __init__(self, models, selected = 0):
        self.models = models
        self.selected = selected
        self.current_model = None

    def switch_model(self, to_model, from_model):
        self.exit_model(from_model)
        self.enter_model(to_model)

    def exit_model(self, model):
        self.current_model = None

    def enter_model(self, model):
        self.current_model = model
        if isinstance(model, automata.Automata3D):
            model.__init__(model.name, model.x, model.y, model.z, *display_size, model.start_density)
        if isinstance(model, automata.Automata):
            model.__init__(model.name, model.x, model.y, *display_size, model.start_density)


# creates window with GUI selection
    def runGUI(self):
        pygame.init()
        self.font_size = 24
        font = pygame.font.Font("Courier_Prime\CourierPrime-Regular.ttf", self.font_size)
        screen = pygame.display.set_mode(display_size)
        clock = pygame.time.Clock()
        running = True
        space_toggled = False
        space_pressed = False
        right_pressed = False
        left_pressed = False

        while running:
            # rendering
            # fill the screen with a color to wipe away last frame
            screen.fill("Black")
            pressed = pygame.key.get_pressed()
            # pygame.key.set_repeat(False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # HANDLES MODEL SELECTION AND MAIN MENU
            # wraps selected to length of model list
            if self.current_model == None:
                model_names = [m.name for m in self.models]
                line = 0
                for m in model_names:
                    # renders line
                    if line == self.selected:
                        rendered = font.render(f'-<{m}>-', True, "Red")
                    else:
                        rendered = font.render(m, True, "White")
                    # positions and blits line
                    screen.blit(rendered, (display_size[0]/2 - font.size(m)[0]/2, display_size[1]/2-(len(model_names)/2)*font.size(m)[1]+line*font.size(m)[1]))
                    # increments line counter for proper spacing
                    line +=1
                # handles incrementing index for selection
                if pressed[pygame.K_DOWN]:
                    if right_pressed == False:
                        self.selected += 1
                        right_pressed = True
                elif pressed[pygame.K_UP]:
                    if left_pressed == False:
                        self.selected -= 1
                        left_pressed = True
                else:
                    right_pressed = False
                    left_pressed = False
                self.selected =  self.selected%len(self.models)
                # handles starting and switching models
                if pressed[pygame.K_RETURN]:
                    # enters new model if no current, otherwise switch model
                    self.enter_model(self.models[self.selected])
            else:
                # handles input
                # if right arrow pressed, progress forward one step
                if pressed[pygame.K_RIGHT]:
                    if right_pressed == False:
                        right_pressed = True
                        self.current_model.step()
                # use space to toggle run
                elif pressed[pygame.K_SPACE]:
                    self.current_model.step()
                else:
                    # space_pressed = False
                    right_pressed = False
                # render model
                screen.blits(self.current_model.render())
                # exit model
                if pressed[pygame.K_ESCAPE]:
                    self.exit_model(self.current_model)
                # blit fps counter
                # screen.blit(font.render(f"{clock.get_fps():.2f}", True, "Red"), (0,0))
                # blit directions
                screen.blit(font.render("Press right arrow to advance simulation one step", True, "Red"), (0,display_size[1]-40))
                screen.blit(font.render("Or, spacebar to continuously advance", True, "Red"), (0,display_size[1]-20))


            # flip() display to put work on screen
            pygame.display.flip()
            # locks framerate
            clock.tick(30)
        pygame.quit()
#--------------------------------------------------------

gui = Gui(automata.create_models(display_size))
gui.runGUI()
