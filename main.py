from moderngl_window import WindowConfig, run_window_config
from moderngl_window.geometry import quad_fs

class App(WindowConfig):
    window_size, resource_dir = (900, 600), 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = quad_fs() #pantalla
        self.program = self.load_program(vertex_shader =\
                                         'vertex.glsl',\
                                         fragment_shader =\
                                         'fragment.glsl')
        self.set_uniform('u_resolution', self.window_size)        

    def set_uniform(self, u_name, u_value):
        try:
            self.program[u_name] = u_value

        except KeyError:
            pass
            #print(f'{u_name} not used in shader')

    def render(self, time, frame_time):
        self.ctx.clear()
        self.set_uniform('u_time', time)
        self.quad.render(self.program)

run_window_config(App)
        
