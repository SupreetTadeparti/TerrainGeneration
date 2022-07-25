#version 330 core

in vec3 v_Normal;
in vec4 v_Color;
in float v_Visibility;
in float v_FragY;

out vec4 o_Color;

uniform float u_Noise;

void main()
{
    vec3 norm = normalize(v_Normal) * 1.5;
    vec3 lightDir = vec3(0.5, -1.0, 0.0);
    float diff = max(dot(norm, lightDir), 0.0) * 5;
    vec3 diffuse = (diff + 2) * vec3(1.0, 1.0, 1.0) / 10;
    vec4 color = vec4(v_Color.rgb - v_FragY / 500 - u_Noise / 255, 1.0);
    o_Color = mix(vec4(0.3, 0.5, 0.8, 1.0), vec4(diffuse, 1.0) * color, v_Visibility);
}