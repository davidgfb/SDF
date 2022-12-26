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

        float dot2(in vec3 v) {return dot(v, v);}

        float udQuad(vec3 v1, vec3 v2, vec3 v3, vec3 v4, vec3 p) {
            #if 1
            // handle ill formed quads
            if( dot( cross( v2-v1, v4-v1 ), cross( v4-v3, v2-v3 )) < 0.0 )
            {
                vec3 tmp = v3;
                v3 = v4;
                v4 = tmp;
            }
            #endif

            
            vec3 v21 = v2 - v1, p1 = p - v1, v32 = v3 - v2, p2 = p - v2, v43 = v4 - v3, p3 = p - v3, v14 = v1 - v4, 
                 p4 = p - v4;
            vec3 nor = cross( v21, v14 );

            return sqrt( (sign(dot(cross(v21,nor),p1)) + 
                          sign(dot(cross(v32,nor),p2)) + 
                          sign(dot(cross(v43,nor),p3)) + 
                          sign(dot(cross(v14,nor),p4))<3.0) 
                          ?
                          min( min( dot2(v21*clamp(dot(v21,p1)/dot2(v21),0.0,1.0)-p1), 
                                    dot2(v32*clamp(dot(v32,p2)/dot2(v32),0.0,1.0)-p2) ), 
                               min( dot2(v43*clamp(dot(v43,p3)/dot2(v43),0.0,1.0)-p3),
                                    dot2(v14*clamp(dot(v14,p4)/dot2(v14),0.0,1.0)-p4) ))
                          :
                          dot(nor,p1)*dot(nor,p1)/dot2(nor) );
        }


        float map(in vec3 p) {
            return udQuad(vec3(1, 0,0), vec3(0,1,0), vec3(0,0, 1), vec3(1,-1,1), p) - 0.01; //0.5
        }

        float intersect(vec3 ro, vec3 rd) {
                float maxd = 10.0, h = 1.0, t = 0.0;
            
            for(int i=0; i<50; i++) {
                if(!(h<0.001 || t>maxd)) {
                    t += map(rd*t + ro);
                }
            }

            if(t>maxd) t=-1.0;
                
            return t;
        }

        const vec3 lig = normalize(vec3(1.0,0.9,0.7));

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

        void main() { //color basado en la posicion del pixel en la pantalla 
            vec3 col = vec3(0), ro = vec3(0, 0, -1), rd = normalize(vec3((2 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y, 1)); //inicia negro, centra el origen de la pantalla, origen_Rayo, dir_Rayo
            float dist = rayMarch(ro, rd); //dist al obj

            if (dist < 100) col += (map(get_P(dist, rd, ro)) + 1) / 2; //suma la distancia al color resultante
            
            fragColor = vec4(col, 1);
        }''') #pantalla

        self.program['u_resolution'] = self.window_size
        
    def render(self, time, frame_time):
        self.ctx.clear()       
        self.quad.render(self.program) #uniform tiene q estar inicializado en glsl

h, es_Primera_Vez = 0, True
run_window_config(App)




'''float map(vec3 p, vec3 a, vec3 b, vec3 c, vec3 d) {
                vec3 ba = b - a, pa = p - a, cb = c - b,\
                     pb = p - b, dc = d - c, pc = p - c,\
                     ad = a - d, pd = p - d;
                vec3 nor = cross(ba, ad);

                return sqrt((sign(dot(cross(ba,nor),pa)) +
                       sign(dot(cross(cb, nor), pb)) +
                       sign(dot(cross(dc, nor), pc)) +
                       sign(dot(cross(ad, nor), pd)) < 3.0) ?
                       min(min(min(dot2(ba * clamp(dot(ba, pa) / dot2(ba), 0.0, 1.0) - pa),
                       dot2(cb * clamp(dot(cb, pb)/dot2(cb), 0.0, 1.0) - pb)),
                       dot2(dc * clamp(dot(dc, pc)/dot2(dc), 0.0, 1.0) - pc)),
                       dot2(ad * clamp(dot(ad, pd)/dot2(ad), 0.0, 1.0) - pd)) :
                       dot(nor, pa) * dot(nor, pa) / dot2(nor));
            } //sdf quad


'''




        
