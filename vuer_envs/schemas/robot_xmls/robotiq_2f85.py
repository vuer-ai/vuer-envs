from ..schema import Body


class Robotiq2F85(Body):
    """
    This is the Gripper for the Ufactory Xarm7 robot.
    """

    assets: str = "robotiq_2f85"

    _attributes = {
        "name": "base_mount",
        "childclass": "2f85",
        "pos": "0 0 0.007",
    }

    _preamble = """
    <option cone="elliptic" impratio="10"/>

    <asset>
      <material name="metal" rgba="0.58 0.58 0.58 1"/>
      <material name="silicone" rgba="0.1882 0.1882 0.1882 1"/>
      <material name="gray" rgba="0.4627 0.4627 0.4627 1"/>
      <material name="black" rgba="0.149 0.149 0.149 1"/>

      <mesh class="{childclass}" file="{assets}/base_mount.stl"/>
      <mesh class="{childclass}" file="{assets}/base.stl"/>
      <mesh class="{childclass}" file="{assets}/driver.stl"/>
      <mesh class="{childclass}" file="{assets}/coupler.stl"/>
      <mesh class="{childclass}" file="{assets}/follower.stl"/>
      <mesh class="{childclass}" file="{assets}/pad.stl"/>
      <mesh class="{childclass}" file="{assets}/silicone_pad.stl"/>
      <mesh class="{childclass}" file="{assets}/spring_link.stl"/>
    </asset>

    <default>
      <default class="{childclass}">
        <mesh scale="0.001 0.001 0.001"/>
        <general biastype="affine"/>

        <joint axis="1 0 0"/>
        <default class="{childclass}-driver">
          <joint range="0 0.8" armature="0.005" damping="0.1" solimplimit="0.95 0.99 0.001" solreflimit="0.005 1"/>
        </default>
        <default class="{childclass}-follower">
          <joint range="-0.872664 0.872664" armature="0.001" pos="0 -0.018 0.0065" solimplimit="0.95 0.99 0.001" solreflimit="0.005 1"/>
        </default>
        <default class="{childclass}-spring_link">
          <joint range="-0.29670597283 0.8" armature="0.001" stiffness="0.05" springref="2.62" damping="0.00125"/>
        </default>
        <default class="{childclass}-coupler">
          <joint range="-1.57 0" armature="0.001" solimplimit="0.95 0.99 0.001" solreflimit="0.005 1"/>
        </default>

        <default class="{childclass}-visual">
          <geom type="mesh" contype="0" conaffinity="0" group="2"/>
        </default>
        <default class="{childclass}-collision">
          <geom type="mesh" group="3"/>
          <default class="{childclass}-pad_box1">
            <geom mass="0" type="box" pos="0 -0.0026 0.028125" size="0.011 0.004 0.009375" friction="0.7"
              solimp="0.95 0.99 0.001" solref="0.004 1" priority="1" rgba="0.55 0.55 0.55 1"/>
          </default>
          <default class="{childclass}-pad_box2">
            <geom mass="0" type="box" pos="0 -0.0026 0.009375" size="0.011 0.004 0.009375" friction="0.6"
              solimp="0.95 0.99 0.001" solref="0.004 1" priority="1" rgba="0.45 0.45 0.45 1"/>
          </default>
        </default>
      </default>
    </default>
    """

    _children_raw = """
    <geom class="{childclass}-visual" mesh="base_mount" material="black"/>
    <geom class="{childclass}-collision" mesh="base_mount"/>
    <body name="{name}-base" pos="0 0 0.0038" quat="1 0 0 -1">
      <inertial mass="0.777441" pos="0 -2.70394e-05 0.0354675" quat="1 -0.00152849 0 0"
        diaginertia="0.000260285 0.000225381 0.000152708"/>
      <geom class="{childclass}-visual" mesh="base" material="black"/>
      <geom class="{childclass}-collision" mesh="base"/>
      <site name="{name}-pinch" pos="0 0 0.145" type="sphere" group="5" rgba="0.9 0.9 0.9 1" size="0.005"/>
      <!-- Right-hand side 4-bar linkage -->
      <body name="{name}-right_driver" pos="0 0.0306011 0.054904">
        <inertial mass="0.00899563" pos="2.96931e-12 0.0177547 0.00107314" quat="0.681301 0.732003 0 0"
          diaginertia="1.72352e-06 1.60906e-06 3.22006e-07"/>
        <joint name="{name}-right_driver_joint" class="{childclass}-driver"/>
        <geom class="{childclass}-visual" mesh="driver" material="gray"/>
        <geom class="{childclass}-collision" mesh="driver"/>
        <body name="{name}-right_coupler" pos="0 0.0315 -0.0041">
          <inertial mass="0.0140974" pos="0 0.00301209 0.0232175" quat="0.705636 -0.0455904 0.0455904 0.705636"
            diaginertia="4.16206e-06 3.52216e-06 8.88131e-07"/>
          <joint name="{name}-right_coupler_joint" class="{childclass}-coupler"/>
          <geom class="{childclass}-visual" mesh="coupler" material="black"/>
          <geom class="{childclass}-collision" mesh="coupler"/>
        </body>
      </body>
      <body name="{name}-right_spring_link" pos="0 0.0132 0.0609">
        <inertial mass="0.0221642" pos="-8.65005e-09 0.0181624 0.0212658" quat="0.663403 -0.244737 0.244737 0.663403"
          diaginertia="8.96853e-06 6.71733e-06 2.63931e-06"/>
        <joint name="{name}-right_spring_link_joint" class="{childclass}-spring_link"/>
        <geom class="{childclass}-visual" mesh="spring_link" material="black"/>
        <geom class="{childclass}-collision" mesh="spring_link"/>
        <body name="{name}-right_follower" pos="0 0.055 0.0375">
          <inertial mass="0.0125222" pos="0 -0.011046 0.0124786" quat="1 0.1664 0 0"
            diaginertia="2.67415e-06 2.4559e-06 6.02031e-07"/>
          <joint name="{name}-right_follower_joint" class="{childclass}-follower"/>
          <geom class="{childclass}-visual" mesh="follower" material="black"/>
          <geom class="{childclass}-collision" mesh="follower"/>
          <body name="{name}-right_pad" pos="0 -0.0189 0.01352">
            <geom class="{childclass}-pad_box1" name="{name}-right_pad1"/>
            <geom class="{childclass}-pad_box2" name="{name}-right_pad2"/>
            <inertial mass="0.0035" pos="0 -0.0025 0.0185" quat="0.707107 0 0 0.707107"
              diaginertia="4.73958e-07 3.64583e-07 1.23958e-07"/>
            <geom class="{childclass}-visual" mesh="pad"/>
            <body name="{name}-right_silicone_pad">
              <geom class="{childclass}-visual" mesh="silicone_pad" material="black"/>
            </body>
          </body>
        </body>
      </body>
      <!-- Left-hand side 4-bar linkage -->
      <body name="{name}-left_driver" pos="0 -0.0306011 0.054904" quat="0 0 0 1">
        <inertial mass="0.00899563" pos="0 0.0177547 0.00107314" quat="0.681301 0.732003 0 0"
          diaginertia="1.72352e-06 1.60906e-06 3.22006e-07"/>
        <joint name="{name}-left_driver_joint" class="{childclass}-driver"/>
        <geom class="{childclass}-visual" mesh="driver" material="gray"/>
        <geom class="{childclass}-collision" mesh="driver"/>
        <body name="{name}-left_coupler" pos="0 0.0315 -0.0041">
          <inertial mass="0.0140974" pos="0 0.00301209 0.0232175" quat="0.705636 -0.0455904 0.0455904 0.705636"
            diaginertia="4.16206e-06 3.52216e-06 8.88131e-07"/>
          <joint name="{name}-left_coupler_joint" class="{childclass}-coupler"/>
          <geom class="{childclass}-visual" mesh="coupler" material="black"/>
          <geom class="{childclass}-collision" mesh="coupler"/>
        </body>
      </body>
      <body name="{name}-left_spring_link" pos="0 -0.0132 0.0609" quat="0 0 0 1">
        <inertial mass="0.0221642" pos="-8.65005e-09 0.0181624 0.0212658" quat="0.663403 -0.244737 0.244737 0.663403"
          diaginertia="8.96853e-06 6.71733e-06 2.63931e-06"/>
        <joint name="{name}-left_spring_link_joint" class="{childclass}-spring_link"/>
        <geom class="{childclass}-visual" mesh="spring_link" material="black"/>
        <geom class="{childclass}-collision" mesh="spring_link"/>
        <body name="{name}-left_follower" pos="0 0.055 0.0375">
          <inertial mass="0.0125222" pos="0 -0.011046 0.0124786" quat="1 0.1664 0 0"
            diaginertia="2.67415e-06 2.4559e-06 6.02031e-07"/>
          <joint name="{name}-left_follower_joint" class="{childclass}-follower"/>
          <geom class="{childclass}-visual" mesh="follower" material="black"/>
          <geom class="{childclass}-collision" mesh="follower"/>
          <body name="{name}-left_pad" pos="0 -0.0189 0.01352">
            <geom class="{childclass}-pad_box1" name="{name}-left_pad1"/>
            <geom class="{childclass}-pad_box2" name="{name}-left_pad2"/>
            <inertial mass="0.0035" pos="0 -0.0025 0.0185" quat="1 0 0 1"
              diaginertia="4.73958e-07 3.64583e-07 1.23958e-07"/>
            <geom class="{childclass}-visual" mesh="pad"/>
            <body name="{name}-left_silicone_pad">
              <geom class="{childclass}-visual" mesh="silicone_pad" material="black"/>
            </body>
          </body>
        </body>
      </body>
    </body>
    """

    _postamble = """
    <contact>
      <exclude body1="{name}-base" body2="{name}-left_driver"/>
      <exclude body1="{name}-base" body2="{name}-right_driver"/>
      <exclude body1="{name}-base" body2="{name}-left_spring_link"/>
      <exclude body1="{name}-base" body2="{name}-right_spring_link"/>
      <exclude body1="{name}-right_coupler" body2="{name}-right_follower"/>
      <exclude body1="{name}-left_coupler" body2="{name}-left_follower"/>
    </contact>

    <!--
      This adds stability to the model by having a tendon that distributes the forces between both
      joints, such that the equality constraint doesn't have to do that much work in order to equalize
      both joints. Since both joints share the same sign, we split the force between both equally by
      setting coef=0.5
    -->
    <tendon>
      <fixed name="{name}-split">
        <joint joint="{name}-right_driver_joint" coef="0.5"/>
        <joint joint="{name}-left_driver_joint" coef="0.5"/>
      </fixed>
    </tendon>

    <equality>
      <connect anchor="0 0 0" body1="{name}-right_follower" body2="{name}-right_coupler" solimp="0.95 0.99 0.001" solref="0.005 1"/>
      <connect anchor="0 0 0" body1="{name}-left_follower" body2="{name}-left_coupler" solimp="0.95 0.99 0.001" solref="0.005 1"/>
      <joint joint1="{name}-right_driver_joint" joint2="{name}-left_driver_joint" polycoef="0 1 0 0 0" solimp="0.95 0.99 0.001"
        solref="0.005 1"/>
    </equality>

    <!--
      The general actuator below is a customized position actuator (with some damping) where
      gainprm[0] != kp (see http://mujoco.org/book/modeling.html#position).
      The reason why gainprm[0] != kp is because the control input range has to be re-scaled to
      [0, 255]. The joint range is currently set at [0, 0.8], the control range is [0, 255] and
      kp = 100. Tau = Kp * scale * control_input - Kp * error, max(Kp * scale * control_input) = 0.8,
      hence scale = 0.8 * 100 / 255
    -->
    <actuator>
      <general class="{childclass}" name="{name}-fingers_actuator" tendon="{name}-split" forcerange="-5 5" ctrlrange="0 255"
        gainprm="0.3137255 0 0" biasprm="0 -100 -10"/>
    </actuator>
    """
