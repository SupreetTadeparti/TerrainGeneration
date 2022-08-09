#version 330 core

in vec3 v_Normal;
in vec3 v_FragPos;
in float v_Visibility;

out vec4 o_Color;

uniform float u_Noise;
uniform float u_OffsetX;
uniform float u_OffsetZ;

#include Noise

void main()
{
    vec3 norm = normalize(v_Normal / 2);
    vec3 lightDir = normalize(vec3(0.5, -1, 0));
    float diff = max(dot(norm, lightDir), 0.0) * 10.0 + 2.0;
    vec3 diffuse = diff * vec3(1.0, 1.0, 1.0) / 10;
    vec4 skyColor = vec4(0.3, 0.5, 0.8, 1.0);
    vec4 waterColor = vec4(0.0, 0.77, 1.0, 0.5);
    float yPos = snoise(vec2(v_FragPos.x / 200 + u_OffsetX, v_FragPos.z / 200 + u_OffsetZ)) * u_Noise + 25;
    yPos += cnoise(vec2(v_FragPos.x / 200 + u_OffsetX, v_FragPos.z / 200 + u_OffsetZ)) * u_Noise * 2 + 10;
    // if (abs(yPos - v_FragPos.y) < 1) 
    //     waterColor = vec4(238.0 / 255.0, 208.0 / 255.0, 171.0 / 255.0, 1.0);
    o_Color = mix(skyColor, vec4(diffuse, 1.0) * waterColor, v_Visibility);
}