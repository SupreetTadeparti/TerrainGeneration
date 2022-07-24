#version 330 core

layout (location = 0) in vec2 position;

out vec4 vary_Color;
out vec4 vary_WorldPos;
out float vary_Visibility;

uniform float u_Noise;
uniform float u_OffsetX;
uniform float u_OffsetZ;
uniform mat4 u_Model;
uniform mat4 u_ViewTranslation;
uniform mat4 u_ViewRotation;
uniform mat4 u_Projection;

const float density = 0.0015;
const float gradient = 5.0;

vec4 mod289(vec4 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec3 mod289(vec3 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec2 mod289(vec2 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 taylorInvSqrt(vec4 r)
{
  return 1.79284291400159 - 0.85373472095314 * r;
}

vec2 fade(vec2 t) {
  return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

vec3 permute(vec3 x) {
  return mod289(((x * 34.0) + 10.0) * x);
}

vec4 permute(vec4 x)
{
  return mod289(((x * 34.0) + 10.0) * x);
}

float snoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
    vec2 i  = floor(v + dot(v, C.yy) );
    vec2 x0 = v - i + dot(i, C.xx);

    vec2 i1;
    i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;

    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0 ));

    vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
    m *= m ;
    m *= m ;

    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;

    m *= 1.79284291400159 - 0.85373472095314 * ( a0 * a0 + h * h );

    vec3 g;
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;

    return 130.0 * dot(m, g);
}

float cnoise(vec2 P)
{
  vec4 Pi = floor(P.xyxy) + vec4(0.0, 0.0, 1.0, 1.0);
  vec4 Pf = fract(P.xyxy) - vec4(0.0, 0.0, 1.0, 1.0);
  Pi = mod289(Pi);
  vec4 ix = Pi.xzxz;
  vec4 iy = Pi.yyww;
  vec4 fx = Pf.xzxz;
  vec4 fy = Pf.yyww;

  vec4 i = permute(permute(ix) + iy);

  vec4 gx = fract(i * (1.0 / 41.0)) * 2.0 - 1.0 ;
  vec4 gy = abs(gx) - 0.5 ;
  vec4 tx = floor(gx + 0.5);
  gx = gx - tx;

  vec2 g00 = vec2(gx.x,gy.x);
  vec2 g10 = vec2(gx.y,gy.y);
  vec2 g01 = vec2(gx.z,gy.z);
  vec2 g11 = vec2(gx.w,gy.w);

  vec4 norm = taylorInvSqrt(vec4(dot(g00, g00), dot(g01, g01), dot(g10, g10), dot(g11, g11)));
  g00 *= norm.x;  
  g01 *= norm.y;  
  g10 *= norm.z;  
  g11 *= norm.w;  

  float n00 = dot(g00, vec2(fx.x, fy.x));
  float n10 = dot(g10, vec2(fx.y, fy.y));
  float n01 = dot(g01, vec2(fx.z, fy.z));
  float n11 = dot(g11, vec2(fx.w, fy.w));

  vec2 fade_xy = fade(Pf.xy);
  vec2 n_x = mix(vec2(n00, n01), vec2(n10, n11), fade_xy.x);
  float n_xy = mix(n_x.x, n_x.y, fade_xy.y);
  return 2.3 * n_xy;
}

void main()
{
    vec4 modelPosition = vec4(position.x, 0, position.y, 1.0);
    vec4 worldPosition = u_Model * modelPosition;
    float yPos = snoise(vec2(worldPosition.x / 200 + u_OffsetX, worldPosition.z / 200 + u_OffsetZ)) * u_Noise + 25;
    yPos += cnoise(vec2(worldPosition.x / 200 + u_OffsetX, worldPosition.z / 200 + u_OffsetZ)) * u_Noise * 2 + 25;
    worldPosition.y = yPos;
    mat4 translation = u_ViewTranslation;
    float cameraYPos = snoise(vec2(-translation[3][0] / 200 + u_OffsetX, -translation[3][2] / 200 + u_OffsetZ)) * u_Noise + 30;
    translation[3][1] = min(translation[3][1], -cameraYPos);
    vec4 viewWorldPosition = u_ViewRotation * translation * worldPosition;
    gl_Position = u_Projection * viewWorldPosition;
    vec4 color = (worldPosition.y < 5) ? vec4(0.5, 0.3, 0.2, 1.0) : vec4(0.4, 0.8, 0.3, 1.0);
    vary_Color = color;
    vary_WorldPos = worldPosition;
    vary_Visibility = clamp(exp(-pow((length(viewWorldPosition.xyz) * density), gradient)), 0.0, 1.0);
}