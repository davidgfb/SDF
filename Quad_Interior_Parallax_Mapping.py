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

            float dot2(in vec3 v) {return dot(v, v);}

            float udQuad(vec3 v1, vec3 v2, vec3 v3, vec3 v4,
                         vec3 p) {       
                // handle ill formed quads
                if(dot(cross(v2 - v1, v4 - v1),
                   cross(v4 - v3, v2 - v3)) < 0) {
                    vec3 tmp = v3;
                    v3 = v4;
                    v4 = tmp;
                }
                            
                vec3 v21 = v2 - v1, p1 = p - v1, v32 = v3 - v2,
                     p2 = p - v2, v43 = v4 - v3, p3 = p - v3,
                     v14 = v1 - v4, p4 = p - v4,
                     nor = cross(v21, v14);

                return sqrt((sign(dot(cross(v21, nor), p1)) + 
                       sign(dot(cross(v32, nor), p2)) + 
                       sign(dot(cross(v43, nor), p3)) + 
                       sign(dot(cross(v14, nor), p4)) < 3) ?
                       min(min(dot2(v21 * clamp(dot(v21, p1) / dot2(v21), 0, 1) - p1), 
                       dot2(v32 * clamp(dot(v32, p2) / dot2(v32), 0, 1) - p2)), 
                       min(dot2(v43 * clamp(dot(v43, p3) / dot2(v43), 0, 1) - p3),
                       dot2(v14 * clamp(dot(v14, p4) / dot2(v14), 0, 1) - p4))) :
                       dot(nor, p1) * dot(nor, p1) / dot2(nor));
            }

            float map(in vec3 p) {
                vec3 v1 = vec3(1, 0,0), v2 = vec3(0,1,0),
                     v3 = vec3(0,0, 1), v4 = vec3(1,-1,1);
                         
                // handle ill formed quads
                if(dot(cross(v2 - v1, v4 - v1),
                   cross(v4 - v3, v2 - v3)) < 0) {
                    vec3 tmp = v3;
                    v3 = v4;
                    v4 = tmp;
                }
                            
                vec3 v21 = v2 - v1, p1 = p - v1, v32 = v3 - v2,
                     p2 = p - v2, v43 = v4 - v3, p3 = p - v3,
                     v14 = v1 - v4, p4 = p - v4,
                     nor = cross(v21, v14);

                return sqrt((sign(dot(cross(v21, nor), p1)) + 
                       sign(dot(cross(v32, nor), p2)) + 
                       sign(dot(cross(v43, nor), p3)) + 
                       sign(dot(cross(v14, nor), p4)) < 3) ?
                       min(min(dot2(v21 * clamp(dot(v21, p1) / dot2(v21), 0, 1) - p1), 
                       dot2(v32 * clamp(dot(v32, p2) / dot2(v32), 0, 1) - p2)), 
                       min(dot2(v43 * clamp(dot(v43, p3) / dot2(v43), 0, 1) - p3),
                       dot2(v14 * clamp(dot(v14, p4) / dot2(v14), 0, 1) - p4))) :
                       dot(nor, p1) * dot(nor, p1) / dot2(nor)) - 0.01; //0.5    
            }

            vec3 get_P(float dist, vec3 rd, vec3 ro) {
                return dist * rd + ro;
            }

            void main() { //color basado en la posicion del pixel en la pantalla 
                vec3 col = vec3(0), ro = vec3(0, 0, -1),
                     rd = normalize(vec3((2 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y, 1)); //inicia negro, centra el origen de la pantalla, origen_Rayo, dir_Rayo

                float dist = 0;

                for (int i = 0; i < 256; i++) {
                    float hit = map(get_P(dist, rd, ro)); //vector p, distancia mas corta al obj
                    dist += hit;

                    if (dist > 100 || abs(hit) < 1e-4) i = 256; //rompe bucle cuando esta lo suf cerca del obj o cuando el rayo escapa de la escena
                }

                if (dist < 100) col += (map(get_P(dist, rd, ro)) + 1) / 2; //suma la distancia al color resultante
                
                fragColor = vec4(col, 1);
            }''') #pantalla

        self.program['u_resolution'] = self.window_size
        
    def render(self, time, frame_time):
        self.ctx.clear()       
        self.quad.render(self.program) #uniform tiene q estar inicializado en glsl

h, es_Primera_Vez = 0, True
run_window_config(App)
