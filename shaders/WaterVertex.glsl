#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in float delta;

uniform float u_DeltaTime;

void main()
{
    float posY = sin(delta + u_DeltaTime * 3);
    gl_Position = vec4(position.x, posY, position.y, 1.0);
}