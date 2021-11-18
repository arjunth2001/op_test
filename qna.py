from transformers import AutoTokenizer
import torch
from datasets import Dataset
import pandas as pd
from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer
from transformers import default_data_collator
import torch
import numpy as np
import streamlit as st


def qna():
    model_checkpoint = "arjunth2001/priv_qna"
    max_answer_length = 30
    n_best_size = 20
    max_length = 384
    doc_stride = 128
    st.subheader(
        "Privacy Policy QnA: Give a Policy and a Question.. Get an answer !")
    with st.form(key='my_form'):
        context = st.text_area('Enter the Privacy Policy', height=300)
        question = st.text_area('Enter the Question')
        get_answer = st.form_submit_button('Get the answer!')
        if get_answer:
            with st.spinner("Finding an Answer..."):
                tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
                pad_on_right = tokenizer.padding_side == "right"

                def prepare_validation_features(examples):
                    examples["question"] = [q.lstrip()
                                            for q in examples["question"]]
                    tokenized_examples = tokenizer(
                        examples["question" if pad_on_right else "context"],
                        examples["context" if pad_on_right else "question"],
                        truncation="only_second" if pad_on_right else "only_first",
                        max_length=max_length,
                        stride=doc_stride,
                        return_overflowing_tokens=True,
                        return_offsets_mapping=True,
                        padding="max_length",
                    )
                    sample_mapping = tokenized_examples.pop(
                        "overflow_to_sample_mapping")
                    tokenized_examples["example_id"] = []

                    for i in range(len(tokenized_examples["input_ids"])):
                        sequence_ids = tokenized_examples.sequence_ids(i)
                        context_index = 1 if pad_on_right else 0
                        sample_index = sample_mapping[i]
                        tokenized_examples["example_id"].append(
                            examples["id"][sample_index])
                        tokenized_examples["offset_mapping"][i] = [
                            (o if sequence_ids[k] == context_index else None)
                            for k, o in enumerate(tokenized_examples["offset_mapping"][i])
                        ]

                    return tokenized_examples
                examples = {
                    "id": [0],
                    "question": [question],
                    "context": [context]
                }
                datasets = Dataset.from_pandas(pd.DataFrame(examples))
                validation_features = datasets.map(
                    prepare_validation_features,
                    batched=True,
                    remove_columns=datasets.column_names
                )
                model = AutoModelForQuestionAnswering.from_pretrained(
                    model_checkpoint)
                args = TrainingArguments(
                    ".",
                    learning_rate=2e-5,
                    per_device_train_batch_size=2,
                    per_device_eval_batch_size=2,
                    num_train_epochs=3,
                    weight_decay=0.01,
                )
                data_collator = default_data_collator
                trainer = Trainer(
                    model,
                    args,
                    train_dataset=validation_features,
                    data_collator=data_collator,
                    tokenizer=tokenizer,
                )
                raw_predictions = trainer.predict(validation_features)
                validation_features.set_format(type=validation_features.format["type"], columns=list(
                    validation_features.features.keys()))
                for batch in trainer.get_train_dataloader():
                    break
                batch = {k: v.to(trainer.args.device)
                         for k, v in batch.items()}
                with torch.no_grad():
                    output = trainer.model(**batch)
                output.keys()
                start_logits = output.start_logits[0].cpu().numpy()
                end_logits = output.end_logits[0].cpu().numpy()
                offset_mapping = validation_features[0]["offset_mapping"]
                context = datasets[0]["context"]
                start_indexes = np.argsort(
                    start_logits)[-1: -n_best_size - 1: -1].tolist()
                end_indexes = np.argsort(
                    end_logits)[-1: -n_best_size - 1: -1].tolist()
                valid_answers = []
                for start_index in start_indexes:
                    for end_index in end_indexes:
                        if (
                            start_index >= len(offset_mapping)
                            or end_index >= len(offset_mapping)
                            or offset_mapping[start_index] is None
                            or offset_mapping[end_index] is None
                        ):
                            continue
                        if end_index < start_index or end_index - start_index + 1 > max_answer_length:
                            continue
                        if start_index <= end_index:
                            start_char = offset_mapping[start_index][0]
                            end_char = offset_mapping[end_index][1]
                            valid_answers.append(
                                {
                                    "score": start_logits[start_index] + end_logits[end_index],
                                    "text": context[start_char: end_char]
                                }
                            )
                valid_answers = sorted(valid_answers, key=lambda x: x["score"], reverse=True)[
                    :n_best_size]
                answer = valid_answers[0]["text"]
            st.success("Answer!")
            st.write(answer)
