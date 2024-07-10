elif choice == "Image":
        st.write("##### :orange[Architecture]")
        st.image("static/image-summary.jpg", width=700)
        image_text = ""
        image_written_text = ""
 
        # Upload a picture for explanation
 
        uploaded_file = st.file_uploader("Upload an image", type=["JPG", "JPEG", "PNG"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
            file_details = {
                "FileName": uploaded_file.name,
                "FileType": uploaded_file.type,
            }
            file_name = uploaded_file.name
 
            with open(os.path.join("data", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
 
            image_file = "data/" + file_name
 
            ts_string = datetime.datetime.fromtimestamp(time.time()).strftime(
                "%Y-%m-%d-%H:%M:%S"
            )
            with open(image_file, "rb") as image:
                # Call Amazon Rekognition DetectLabels API to detect labels in image
                response = rekognition.detect_labels(Image={"Bytes": image.read()})
 
            for label in response["Labels"]:
                if label["Confidence"] > 80:
                    image_text = image_text + " " + label["Name"]
 
            with open(image_file, "rb") as image:
                response = rekognition.detect_text(Image={"Bytes": image.read()})
 
            for text in response["TextDetections"]:
                if text["Type"] == "LINE":
                    image_written_text = image_written_text + " " + text["DetectedText"]
 
            complete_text = image_text + image_written_text
 
            show_summary_prompt = st.checkbox("##### :green[Show prompt]", value=True)
 
            if show_summary_prompt:
                st.code(image_prompt)
 
            claude_prompt = image_prompt + complete_text
            claude_response, claude_metadata = call_claude_v3_sonet(
                claude_prompt, 0.1, 500
            )
            write_stream(claude_response)
            # Enable for Troubleshooting
            # print(claude_metadata)
 
            # Call Function with specific key declared as variable for input and output token
            st.write(
                "####### :red[Input Token Count:]",
                get_tokencount(claude_metadata, get_input_token),
            )
            st.write(
                "###### :red[Output Token Count:]",
                get_tokencount(claude_metadata, get_output_token),
            )
 
            # Save summary to s3
            if "Unable to invoke the model" not in claude_response:
                file_key = model_summary_suffix + "-summary-" + ts_string
                summary_file = s3.Object(
                    bucket_name=summary_bucket,
                    key=text_summary_folder + file_key + ".txt",
                )
                summary_file.put(Body=claude_response)
                put_parameter("/genai_app/last_summary", file_key)
            else:
                print("No response from model")
 
            file_key = get_parameter("/genai_app/last_summary")
            read_summary(
                summary_bucket, text_summary_folder, file_key, audio_summary_folder
            )
 
            input_prompt = get_custom_prompt()
            if st.button("###### :blue[Summarize with custom prompt]"):
                with st.spinner("Generating summary ..."):
                    claude_prompt = input_prompt + "\n\n" + complete_text
                    claude_response, claude_metadata = call_claude_v3_sonet(
                        claude_prompt, temperature, max_tokens
                    )
                    write_stream(claude_response)
                    # Enable for Troubleshooting
                    # print(claude_metadata)
 
                    # Call Function with specific key declared as variable for input and output token
                    st.write(
                        "####### :red[Input Token Count:]",
                        get_tokencount(claude_metadata, get_input_token),
                    )
                    st.write(
                        "###### :red[Output Token Count:]",
                        get_tokencount(claude_metadata, get_output_token),
                    )
 
                # Save summary to s3
                if "Unable to invoke the model" not in claude_response:
                    file_key = model_summary_suffix + "-summary-" + ts_string
                    summary_file = s3.Object(
                        bucket_name=summary_bucket,
                        key=text_summary_folder + file_key + ".txt",
                    )
                    summary_file.put(Body=claude_response)
                    put_parameter("/genai_app/last_summary", file_key)
                else:
                    print("No response from model")
 
                file_key = get_parameter("/genai_app/last_summary")
                read_summary(
                    summary_bucket, text_summary_folder, file_key, audio_summary_folder
                )