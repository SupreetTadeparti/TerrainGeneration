#version 330 core

layout (location = 0) in vec4 a_Position;

out vec4 v_FragPos;

uniform mat4 u_Projection;
uniform mat4 u_View;
uniform mat4 u_Model;

void main()
{
    v_FragPos = u_Model * a_Position;
    gl_Position = u_Projection * u_View * v_FragPos;
}