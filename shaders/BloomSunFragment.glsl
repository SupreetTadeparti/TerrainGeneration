#version 330 core

in vec4 v_FragPos;

out vec4 o_Color;

uniform vec3 u_Center;

void main()
{
    o_Color = vec4(1.0f, 1.0f, 0.0f, 0.3);
}