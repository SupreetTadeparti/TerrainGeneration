#version 330 core

in vec3 v_Normal;
in vec3 v_FragPos;
in float v_Visibility;

out vec4 o_Color;

uniform float u_Noise;
uniform float u_OffsetX;
uniform float u_OffsetZ;
uniform vec3 u_SunPos;

#include Noise

void main()
{
    vec3 norm = normalize(v_Normal / 2);
    vec3 lightDir = normalize(-u_SunPos);
    float diff = max(dot(norm, lightDir), 0.0) * 10.0 + 2.0;
    vec3 diffuse = diff * vec3(1.0, 1.0, 1.0) / 10;
    vec4 skyColor = vec4(0.3, 0.5, 0.8, 1.0);
    vec4 waterColor = vec4(0.0, 0.77, 1.0, 0.5);
    o_Color = mix(skyColor, vec4(diffuse, 1.0) * waterColor, v_Visibility);
}