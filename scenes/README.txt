新しいシーン(name:hoge.pbrt)をダウンロードして、dasr用のデータを作成したい場合


1. シーン(hoge.xml)の書き換え
    0. もし、<scene version="0.6.0">でない場合は一度GUIにシーンを読み込ませ、更新
    1. integratorの書き換え

        <integrator type="multichannel">
            <integrator type="path"/>

            <integrator type="field">
                <string name="field" value="shNormal"/>
            </integrator>

            <integrator type="field">
                <string name="field" value="distance"/>
            </integrator>

            <integrator type="field">
                <string name="field" value="albedo"/>
            </integrator>

            <integrator type="direct"/>
	    </integrator>

    2. samplerの書き換え

        <sampler type="independent">
			<integer name="sampleCount" value='@NUMBER_OF_SAMPLES@'/>
		</sampler>

    3. filmの書き換え

		<film type="hdrfilm">
			<string name="channelNames" value="color, normal, distance, albedo, shadow"/>
			<integer name="height" value="512"/>
			<integer name="width" value="512"/>
			<string name="pixelFormat" value="rgb, rgb, luminance, rgb, luminance"/>
		</film>

3. mitsubaでレンダリング
    1. hoge dirでcmdを起動
    2. python ../run_render.py hoge.xml　outputs_dir
