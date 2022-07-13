#version 330 core

layout(location = 0) out float o_Depth;

void main(){
    o_Depth = gl_FragCoord.z;
}