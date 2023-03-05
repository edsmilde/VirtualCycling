#version 330

uniform vec3 u_ambientLightColor;

in vec3 v_fragmentNormal;

out vec4 fragColor;

void main()
{
    // Calculate ambient light contribution
    vec3 ambientLight = u_ambientLightColor * 0.5 + 0.5;

    // Calculate final fragment color
    fragColor = vec4(v_fragmentNormal * ambientLight, 1.0);
}
