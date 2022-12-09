from moderngl_window import WindowConfig, run_window_config
from moderngl_window.geometry import quad_fs

class App(WindowConfig):
    window_size = 900, 600
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad, self.program = quad_fs(),\
                                self.ctx.program(vertex_shader =\
        '''#version 460
        in vec3 in_position; //vertices pantalla

        void main() {
            gl_Position = vec4(in_position, 1); //rasteriza pantalla en fragmentos, vertices --> fragmentos
        }''', fragment_shader =\
        '''#version 460
        out vec4 fragColor; //color para cada fragmento

        uniform vec2 u_resolution;
        uniform float h = 0;

        float map(vec3 p) { //sdf esfera
            return length(p) - 3.0 / 5; //u_resolution.y / u_resolution.x
        }

        vec3 getNormal(vec3 p, vec3 n = vec3(0, 1, 0)) { //sdf plano, en cualquier punto de la superficie del sdf el gradiente es el mismo que la normal del obj en ese punto 
            float sharpness = 10; 
            vec3 color = mix(vec3(0, 1, 0), vec3(1, 0, 0), clamp(sharpness * dot(p, n) - h, 0, 1)); //dot - h entre parentesis sino

            return color;
        }

        vec3 get_P(float dist, vec3 rd, vec3 ro) {
            return dist * rd + ro;
        }

        float rayMarch(vec3 ro, vec3 rd) {
            float dist = 0;

            for (int i = 0; i < 256; i++) {
                float hit = map(get_P(dist, rd, ro)); //vector p, distancia mas corta al obj
                dist += hit;

                if (dist > 100 || abs(hit) < 1e-4) i = 256; //rompe bucle cuando esta lo suf cerca del obj o cuando el rayo escapa de la escena
            }

            return dist;
        }

        vec3 render() { //color basado en la posicion del pixel en la pantalla
            vec3 col = vec3(0), ro = vec3(0, 0, -1), rd = normalize(vec3((2 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y, 1)); //inicia negro, centra el origen de la pantalla, origen_Rayo, dir_Rayo
            float dist = rayMarch(ro, rd); //dist al obj

            if (dist < 100) col += (getNormal(get_P(dist, rd, ro)) + 1) / 2; //suma la distancia al color resultante
                        
            return col;
        }

        void main() {
            fragColor = vec4(render(), 1);
        }
        ''') #pantalla
        self.program['u_resolution'] = self.window_size
        
    def render(self, time, frame_time):
        self.ctx.clear()       
        self.quad.render(self.program) #uniform tiene q estar inicializado en glsl

    def unicode_char_entered(self, char):
        global h

        es_Mas = char == '+'
        
        if es_Mas or char == '-':
            if es_Mas:
                h += 1

            else:
                h -= 1

            self.program['h'] = h            

    '''def mouse_position_event(self, x, y, dx, dy):
        print(x, y)
        #self.program['u_mouse'] = (x, y)'''

h, es_Primera_Vez = 0, True
run_window_config(App)




        
