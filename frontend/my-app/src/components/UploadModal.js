import { Modal } from "antd";

const UploadModal = ({ visible, onCancel }) => {
  return (
    <Modal
      title="File Uploaded"
      visible={visible}
      onCancel={onCancel}
      onOk={onCancel}
    >
      <p>Your file has been uploaded successfully.</p>
    </Modal>
  );
};

export default UploadModal;
