//my
import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  CircularProgress,
  IconButton,
} from '@mui/material';
import { styled } from '@mui/system';
import CloseIcon from '@mui/icons-material/Close';

const StyledContainer = styled(Container)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  padding: '2rem',
});

const StyledPaper = styled(Paper)({
  padding: '2rem',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  minWidth: '80%',
});

const StyledForm = styled('form')({
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
});

const StyledAnswer = styled(Box)({
  marginTop: '2rem',
  textAlign: 'left',
});

const PDFViewer = styled('iframe')({
  marginTop: '2rem',
  minWidth: '100%',
  minHeight: '50vh',
  border: 'none',
});

const CloseButton = styled(IconButton)({
  position: 'absolute',
  right: '1rem',
  top: '1rem',
});

const Chatbot = (props) => {
  const [question, setQuestion] = useState('');
  const [file, setFile] = useState(null);
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPDF, setShowPDF] = useState(false);
  const [pdfURL, setPdfURL] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const serverHost = window.location.hostname;
      const formData = new FormData();
      formData.append('question', question);
      formData.append('file', file);

      const response = await fetch(`http://${serverHost}:5001/chatbot`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const jsonResponse = await response.json();
        setAnswer(jsonResponse.answer);

        if (jsonResponse.highlighted_pdf_path) {
          setShowPDF(true);
          const pageNumber = jsonResponse.page_number || 1;
          setPdfURL(`http://${serverHost}:5001/${jsonResponse.highlighted_pdf_path}#page=${pageNumber}`);
        }
      } else {
        console.error('Error:', response.status, response.statusText);
        setAnswer('No answer found');
      }
    } catch (error) {
      console.error('Error fetching chatbot response', error);
    } finally {
      setIsLoading(false);
      props.onImageFollowMouse();
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleClosePDF = () => {
    setShowPDF(false);
    setPdfURL('');
  };

  return (
    <Box minHeight="100vh">
      <StyledContainer maxWidth="sm">
        <StyledPaper elevation={5}>
          <Typography variant="h4" gutterBottom>
            42
          </Typography>
          <StyledForm onSubmit={handleSubmit}>
            <TextField
              label="Enter your question"
              variant="outlined"
              value={question}
              fullWidth
              onChange={(e) => setQuestion(e.target.value)}
            />
            <input
              accept="application/pdf"
              id="contained-button-file"
              type="file"
              hidden
              onChange={handleFileChange}
            />
            <label htmlFor="contained-button-file">
              <Button variant="contained" color="primary" component="span">
                Upload PDF
              </Button>
            </label>
            <Button variant="contained" color="primary" type="submit" disabled={!file || isLoading}>
              Submit
            </Button>
            {isLoading && <CircularProgress />}
          </StyledForm>
          {answer && (
            <StyledAnswer>
              <Typography variant="h6">Answer:</Typography>
              <Typography>{answer}</Typography>
            </StyledAnswer>
          )}
          {answer && showPDF && (
            <>
              <CloseButton onClick={handleClosePDF}>
                <CloseIcon />
              </CloseButton>
              <PDFViewer key={pdfURL} src={pdfURL} />
            </>
          )}
        </StyledPaper>
      </StyledContainer>
    </Box>
  );
};

export default Chatbot;

