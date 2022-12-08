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
        uniform float u_time;

        float map(vec3 p) { //sdf esfera
            return length(p) - 3.0 / 5;
        }

        vec3 getNormal(vec3 p, vec3 n = vec3(0, 1, 0), float h = 0) { //sdf plano, en cualquier punto de la superficie del sdf el gradiente es el mismo que la normal del obj en ese punto 
            float sharpness = 10, dist = clamp(p.y * sharpness + 1.0 / 2, 0, 1);
            vec3 color = mix(vec3(0, 1, 0), vec3(1, 0, 0), dist);

            /*vec3 color = vec3(1, 0, 0); //rojo
                                                                 
            if (dot(p, n) + h < 0) { //n debe estar normalizada 
                color = vec3(0, 1, 0); //verde
            }*/

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
        
