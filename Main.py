from moderngl_window import WindowConfig, run_window_config
from moderngl_window.geometry import quad_fs

class App(WindowConfig):
    window_size = (900, 600)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = quad_fs() #pantalla
        self.program = self.ctx.program(vertex_shader =\
            '''#version 460
            in vec3 in_position; //vertices pantalla

            void main() {
                gl_Position = vec4(in_position, 1); //rasteriza pantalla en fragmentos, vertices --> fragmentos
            }''', fragment_shader =\
            '''#version 460
            out vec4 fragColor; //color para cada fragmento

            uniform vec2 u_resolution;
            uniform float u_time;
            //uniform sampler2D u_texture1; //?

            mat2 rot2D(float a) {
                float sa = sin(a);
                float ca = cos(a);

                return mat2(ca, sa, -sa, ca);
            }

            /*void rotate(input vec3 p) {
                p.xy *= rot2D(sin(u_time * 0.8) / 4.0);
                p.yz *= rot2D(sin(u_time * 0.7) / 5.0);
            }*/
    
            float map(vec3 p) { //sdf toroide
                return (length(vec2(length(p.xy) - 3 / 5.0,
                       p.z)) - 0.22) * 0.7;
            }

            vec3 getNormal(vec3 p) {
                vec2 e = vec2(0.01, 0);
                vec3 n = vec3(map(p)) - vec3(map(p - e.xyy),
                     map(p - e.yxy), map(p - e.yyx));

                return normalize(n);
            }

            float rayMarch(vec3 ro, vec3 rd) {
                float dist = 0;

                for (int i = 0; i < 256; i++) {
                    vec3 p = dist * rd + ro; //vector p
                    float hit = map(p); //distancia mas corta al obj
                    dist += hit;

                    if (dist > 100 || abs(hit) < 1e-4) i = 256; //rompe bucle cuando esta lo suf cerca del obj o cuando el rayo escapa de la escena
                }

                return dist;
            }

            /*vec3 triPlanar(sampler2D tex, vec3 p, vec3 normal) {
                normal = abs(normal);
                normal = pow(normal, vec3(15));
                normal /= normal.x + normal.y + normal.z;
                p = p / 2.0 + 1 / 2.0;

                return (texture(tex, p.xy) * normal.z +
                        texture(tex, p.xz) * normal.y +
                        texture(tex, p.yz) * normal.x).rgb;
            }*/

            vec3 render() { //color basado en la posicion del pixel en la pantalla
                vec2 uv = (2 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y; //centra el origen de la pantalla
                vec3 col = vec3(0); //inicia negro

                vec3 ro = vec3(0, 0, -1), rd = normalize(vec3(uv, 1)); //origen_Rayo, dir_Rayo
                float dist = rayMarch(ro, rd); //dist al obj

                if (dist < 100) {
                    vec3 p = dist * rd + ro;
                    col += getNormal(p) / 2.0 + 1 / 2.0; //dist; //suma la distancia al color resultante
                }
                
                return col;
            }

            void main() {
                vec3 color = render(); 

                fragColor = vec4(color, 1);
            }''')
        
        self.program['u_resolution'] = self.window_size

    def render(self, time, frame_time):
        self.ctx.clear()
        self.quad.render(self.program)

run_window_config(App)
        
